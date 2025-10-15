import grpc
import hello_pb2
import hello_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50055')
    stub = hello_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(name='Jiten'))
    print("Client received:", response.message)

if __name__ == '__main__':
    run()