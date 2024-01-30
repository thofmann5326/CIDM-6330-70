import pytest
from sqlalchemy.sql import delete, insert, select, text
from allocation.domain import model
from allocation.adapters.orm import allocations, batches
from allocation.service_layer import unit_of_work


def insert_batch(session, ref, sku, qty, eta):
    session.execute(
        insert(batches).values(reference=ref, sku=sku, _purchased_quantity=qty, eta=eta)
    )
    # session.execute(
    #     "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
    #     " VALUES (:ref, :sku, :qty, :eta)",
    #     dict(ref=ref, sku=sku, qty=qty, eta=eta),
    # )


def get_allocated_batch_ref(session, orderid, sku):
    # this is a non-orm approach
    # [[orderlineid]] = session.execute(
    #     "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
    #     dict(orderid=orderid, sku=sku),
    # )

    # SQLAlchemy ORM approach
    orderline = session.scalars(
        select(model.OrderLine)
        .where(model.OrderLine.orderid == orderid)
        .where(model.OrderLine.sku == sku)
    ).first()

    orderlineid = orderline.orderid

    # batchref = session.scalars(
    #     text(
    #         "SELECT b.reference FROM allocations JOIN batches AS b ON batch_id = b.id"
    #         " WHERE orderline_id=:orderlineid"
    #     ),
    #     dict(orderlineid=orderlineid),
    # )

    # SQLAlchmey 2.x join_from
    # https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#setting-the-leftmost-from-clause-in-a-join
    stmt = (
        select(model.Batch.reference)
        .join_from(allocations, batches)
        .where(model.OrderLine.orderid == orderlineid)
    )

    print(f"==============================")
    print(stmt)
    print(f"==============================")

    batchref = session.execute(stmt).scalars().first()

    print(f"==============================")
    print(batchref)
    print(f"==============================")

    session.close()
    return batchref


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory
    insert_batch(session, "batch1", "HIPSTER-WORKBENCH", 100, None)
    session.commit()

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        batch = uow.batches.get(reference="batch1")
        line = model.OrderLine("o1", "HIPSTER-WORKBENCH", 10)
        batch.allocate(line)
        uow.commit()

    batchref = get_allocated_batch_ref(session, "o1", "HIPSTER-WORKBENCH")
    assert batchref == "batch1"
    session.close()


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, "batch1", "MEDIUM-PLINTH", 100, None)

    new_session = session_factory
    rows = list(new_session.execute(text('SELECT * FROM "batches"')))
    assert rows == []
    session_factory.close()
    new_session.close()


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_batch(uow.session, "batch1", "LARGE-FORK", 100, None)
            raise MyException()

    new_session = session_factory
    rows = list(new_session.execute(text('SELECT * FROM "batches"')))
    assert rows == []
    session_factory.close()
    new_session.close()
