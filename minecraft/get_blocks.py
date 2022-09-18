from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import mcpi.minecraft as minecraft
import collections
import select
import socket
import threading
import timeit
from queue import Queue

class Cuboid:
    def __init__(self, x_range, y_range, z_range):
        if x_range[0] >= x_range[1]:
            raise RuntimeError("bad x")
        if y_range[0] >= y_range[1]:
            raise RuntimeError("bad y")
        if z_range[0] >= z_range[1]:
            raise RuntimeError("bad z")
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def __repr__(self):
        return f"({self.x_range}, {self.y_range}, {self.z_range})"

    def generate(self):
        for x in range(*self.x_range):
            for y in range(*self.y_range):
                for z in range(*self.z_range):
                    yield (x, y, z)

    def total_blocks(self):
        return ((self.x_range[1] - self.x_range[0]) * (self.y_range[1] - self.y_range[0]) * (self.z_range[1] - self.z_range[0]))

def query_blocks(requests, fmt, parse_fn, thread_count = 32):
    def worker_fn(mc_socket, request_iter, request_lock, answer_queue,):
        more_requests = True
        request_buffer = bytes()
        response_buffer = bytes()
        pending_request_queue = collections.deque()
        while more_requests or len(pending_request_queue) > 0:
            while more_requests and len(request_buffer) < 4096:
                with request_lock:
                    try:
                        request = next(request_iter)
                    except StopIteration:
                        more_requests = False
                        continue
                    request_buffer = request_buffer + (fmt % request).encode('utf-8') + "\n".encode('utf-8')
                    pending_request_queue.append(request)

            w = [mc_socket] if len(request_buffer) > 0 else []
            r, w, x = select.select([mc_socket], w, [], 5)
            allow_read = bool(r)
            allow_write = bool(w)

            if allow_write:
                bytes_written = mc_socket.send(request_buffer)
                request_buffer = request_buffer[bytes_written:]
                if bytes_written == 0:
                    raise RuntimeError("unexpected socket.send()=0")
            if allow_read:
                bytes_read = mc_socket.recv(1024)
                response_buffer = response_buffer + bytes_read
                if bytes_read == 0:
                    raise RuntimeError("unexpected socket.recv()=0")

            responses = response_buffer.split("\n".encode('utf-8'))
            response_buffer = responses[-1]
            responses = responses[:-1]
            for response_string in responses:
                request = pending_request_queue.popleft()
                answer_queue.put((request, parse_fn(response_string)))

    request_lock = threading.Lock()
    answer_queue = Queue()
    sockets = []

    try:
        for _ in range(thread_count):
            sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            sockets[-1].connect(("localhost", 4711))
        workers = []
        threading.stack_size(128 * 1024)
        for w in range(thread_count):
            t = threading.Thread(target = worker_fn, args = (sockets[w], iter(requests), request_lock, answer_queue))
            t.start()
            workers.append(t)

        for w in workers:
            w.join()
    except socket.error as e:
        print("Socket error:", e)
        raise e
    finally:
        for s in sockets:
            try:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except socket.error as e:
                pass
    while not answer_queue.empty():
        yield answer_queue.get()


def try_multiple_threads_socket_stuffing(input_cuboid):
    my_blocks = {}
    for pos, blk in query_blocks(input_cuboid.generate(), "world.getBlock(%d,%d,%d)", int, thread_count=16):
        my_blocks[pos] = blk
    return my_blocks

# start_block [x,y,z], end_block [x,y,z]
def get_blocks(start_block, end_block):
    try:
        minecraft.Minecraft.create()
    except socket.error as e:
        print("Cannot connect to minecraft server")
        raise e
    
    my_cuboid = Cuboid((start_block[0],end_block[0]), (start_block[1],end_block[1]), (start_block[2],end_block[2]))
    #my_blocks = try_multiple_threads_socket_stuffing(my_cuboid, get_blocks_with_data)

    test_efficiency = True
    if test_efficiency:
        starttime = timeit.default_timer()
        what_test = "multiple_threads_socket_stuffing"
        my_blocks = try_multiple_threads_socket_stuffing(my_cuboid)
        endtime = timeit.default_timer()
        total_block_count = my_cuboid.total_blocks()
        overall_time = endtime - starttime

        print("Total", total_block_count, "blocks in", overall_time, 'seconds using', what_test)
        print("Overall:", total_block_count / overall_time, "blocks/second")

    return my_blocks