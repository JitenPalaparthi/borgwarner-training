import asyncio
import grpc
import sys
sys.path.append("server")  # so we can import generated stubs locally

import customer_pb2 as pb
import customer_pb2_grpc as pb_grpc

ADDR = "localhost:50051"

async def main():
    async with grpc.aio.insecure_channel(ADDR) as channel:
        stub = pb_grpc.CustomerServiceStub(channel)

        # Create
        create_resp = await stub.CreateCustomer(pb.CreateCustomerRequest(
            name="Jiten", email="jiten@example.com", phone="+91-9999999999"
        ))
        cid = create_resp.customer.id
        print("Created:", create_resp.customer)

        # Get
        got = await stub.GetCustomer(pb.GetCustomerRequest(id=cid))
        print("Fetched:", got.customer)

        # Update
        upd = await stub.UpdateCustomer(pb.UpdateCustomerRequest(
            id=cid, name="Jiten P", email="jiten@example.com", phone="+91-8888888888"
        ))
        print("Updated:", upd.customer)

        # List (server streaming)
        print("List (first 5):")
        stream = stub.ListCustomers(pb.ListCustomersRequest(limit=5, offset=0))
        async for c in stream:
            print(" -", c)

        # Delete
        del_resp = await stub.DeleteCustomer(pb.DeleteCustomerRequest(id=cid))
        print("Deleted ok?", del_resp.ok)

if __name__ == "__main__":
    asyncio.run(main())
