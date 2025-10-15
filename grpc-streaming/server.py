import time
from concurrent import futures

import grpc
import chat_pb2
import chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        # Stream: for each incoming message, send a response
        for msg in request_iterator:
            print(f"[Server] from {msg.sender}: {msg.text}")
            yield chat_pb2.ChatMessage(
                sender="server",
                text=f"echo: {msg.text}",
                sent_at_unix=int(time.time()),
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50057")
    print("🚀 gRPC server on :50057")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()