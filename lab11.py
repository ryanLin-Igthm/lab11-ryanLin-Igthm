# Intermediate programming practice: async and sockets.
#
# For EACH problem, work out your problem-solving OUTLINE first, then implement it (you
# may use an AI assistant to help - see the README). The async parts must actually run
# their work CONCURRENTLY (that's the whole point), not one after another.
#
# Do not rename the functions - the tests use these names.

import asyncio
import socket


async def gather_doubled(numbers):
    # Outline (write your plan here first):
    #  input is an list of numbers, output is double the original number
    # Plan: I would first multiply each number by two to double them
    # then I will use asyncio.gather to give me the doubled numbers and put them into a list
    # lasty, return the list.
    #   ...
    # TODO (Part 1, async): run one async task per number that returns n * 2, all
    #   CONCURRENTLY with asyncio.gather, and return the results as a list in the same
    #   order as `numbers`.
    async def double(n):
        return n * 2

    tasks = [double(n) for n in numbers]

    results = await asyncio.gather(*tasks)

    return results


async def fastest(jobs):
    # Outline:
    #   ...
    # Input is a list of jobs with their label and delay, output the label that finish first
    # The plan would be to run each of the jobs at once with asyncio.as_completed()
    # and then wait until 1 of the jobs finished and return that one
    # TODO (Part 2, async): `jobs` is a list of (label, delay) pairs. Start them all
    #   concurrently - each one just does `await asyncio.sleep(delay)` - and return the
    #   label of the FIRST job to finish. (Hint: asyncio.as_completed.)
    async def job(label, delay):
        await asyncio.sleep(delay)
        return label
    
    coros = [job(label, delay) for label, delay in jobs]
    async for coro in asyncio.as_completed(coros):
        return await coro


def echo_once(host, port, message):
    # Outline:
    #   ...
    # Input is a host, port and message, ouput is servers reply message
    # Plan: create a TCP socket and connect it to the host and port
    # then encode the message so that it can be sent and then recieve the reply
    # with recv and lastly, return the reply message and decode it.
    # TODO (Part 3, sockets): open a TCP socket and connect to (host, port). Send
    #   `message` (encode it to bytes first), receive the server's reply, and return it
    #   as a string. (Hint: socket.socket, .connect, .sendall, .recv, .decode.)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode())
        data = sock.recv(1024)
    return data.decode()


def main():
    # Optional scratch space - try the async parts here, e.g.:
    # print(asyncio.run(gather_doubled([1, 2, 3, 4])))   # [2, 4, 6, 8]
    # print(asyncio.run(fastest([("A", 0.06), ("B", 0.02), ("C", 0.04)])))   # returns "B"
    print(echo_once("127.0.0.1", 50011, "hello"))   # returns "hello"   (against an echo server)
    pass


if __name__ == "__main__":
    main()
