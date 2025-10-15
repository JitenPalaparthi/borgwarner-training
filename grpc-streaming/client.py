import time
import threading
import queue

import grpc
import chat_pb2
import chat_pb2_grpc


def request_generator(q: "queue.Queue[chat_pb2.ChatMessage]"):
    """
    Yields ChatMessage objects placed in the queue.
    Put None to signal end-of-stream.
    """
    while True:
        item = q.get()
        if item is None:
            return  # closes client stream
        yield item


def main():
    channel = grpc.insecure_channel("localhost:50055")
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    q: "queue.Queue[chat_pb2.ChatMessage]" = queue.Queue()

    # Start the RPC: returns an iterator for server responses.
    responses = stub.Chat(request_generator(q))

    # Thread to receive and print server messages
    def recv_loop():
        try:
            for r in responses:
                print(f"[Client] got from {r.sender}: {r.text} (t={r.sent_at_unix})")
        except grpc.RpcError as e:
            print(f"[Client] stream ended: {e.code().name}")

    recv_t = threading.Thread(target=recv_loop, daemon=True)
    recv_t.start()

    # Simulate sending a few messages (replace with input() loop if you like)
    me = "jiten"
    for text in ["hi", "how are you?", "bidi streaming is cool", "bye"]:
        msg = chat_pb2.ChatMessage(sender=me, text=text, sent_at_unix=int(time.time()))
        q.put(msg)
        time.sleep(0.5)

    # Close the client stream
    q.put(None)

    # Give a moment to receive any final server messages
    recv_t.join(timeout=2.0)


if __name__ == "__main__":
    main()