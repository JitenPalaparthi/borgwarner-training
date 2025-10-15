import os
import asyncio
import grpc
import asyncpg

from . import customer_pb2 as pb
from . import customer_pb2_grpc as pb_grpc
from .db import init_pool, close_pool, fetchrow, fetch, execute, record_to_customer

PORT = int(os.getenv("PORT", "50051"))

CREATE_SQL = """
INSERT INTO customers (name, email, phone)
VALUES ($1, $2, $3)
RETURNING id, name, email, phone, created_at
"""

GET_SQL = """
SELECT id, name, email, phone, created_at
FROM customers
WHERE id = $1
"""

UPDATE_SQL = """
UPDATE customers
SET name = $2, email = $3, phone = $4
WHERE id = $1
RETURNING id, name, email, phone, created_at
"""

DELETE_SQL = "DELETE FROM customers WHERE id = $1"

LIST_SQL = """
SELECT id, name, email, phone, created_at
FROM customers
ORDER BY created_at DESC
LIMIT $1 OFFSET $2
"""

DEFAULT_LIMIT = 50

class CustomerService(pb_grpc.CustomerServiceServicer):
    async def CreateCustomer(self, request: pb.CreateCustomerRequest, context: grpc.aio.ServicerContext):
        try:
            rec = await fetchrow(CREATE_SQL, request.name, request.email, request.phone)
        except asyncpg.UniqueViolationError:
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, "email already exists")
        except Exception as e:
            await context.abort(grpc.StatusCode.INTERNAL, str(e))

        cust = pb.Customer(**record_to_customer(rec))
        return pb.CustomerResponse(customer=cust)

    async def GetCustomer(self, request: pb.GetCustomerRequest, context: grpc.aio.ServicerContext):
        rec = await fetchrow(GET_SQL, request.id)
        if not rec:
            await context.abort(grpc.StatusCode.NOT_FOUND, "customer not found")
        cust = pb.Customer(**record_to_customer(rec))
        return pb.CustomerResponse(customer=cust)

    async def UpdateCustomer(self, request: pb.UpdateCustomerRequest, context: grpc.aio.ServicerContext):
        rec = await fetchrow(UPDATE_SQL, request.id, request.name, request.email, request.phone)
        if not rec:
            await context.abort(grpc.StatusCode.NOT_FOUND, "customer not found")
        cust = pb.Customer(**record_to_customer(rec))
        return pb.CustomerResponse(customer=cust)

    async def DeleteCustomer(self, request: pb.DeleteCustomerRequest, context: grpc.aio.ServicerContext):
        cmd_tag = await execute(DELETE_SQL, request.id)
        ok = cmd_tag.endswith("1")
        return pb.DeleteCustomerResponse(ok=ok)

    async def ListCustomers(self, request: pb.ListCustomersRequest, context: grpc.aio.ServicerContext):
        limit = request.limit if request.limit > 0 else DEFAULT_LIMIT
        offset = request.offset if request.offset > 0 else 0
        rows = await fetch(LIST_SQL, limit, offset)
        for rec in rows:
            yield pb.Customer(**record_to_customer(rec))


async def serve() -> None:
    await init_pool()
    server = grpc.aio.server()
    pb_grpc.add_CustomerServiceServicer_to_server(CustomerService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    await server.start()
    print(f"🚀 gRPC server listening on :{PORT}")
    try:
        await server.wait_for_termination()
    finally:
        await close_pool()

if __name__ == "__main__":
    asyncio.run(serve())
