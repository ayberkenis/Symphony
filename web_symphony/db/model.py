import logging
import typing as t


class BaseORM:
    def __init__(self, table: str, columns: t.Dict[str, t.Union[str, t.Type]]) -> None:
        self.table = table
        self.columns = columns
        self.logger = logging.getLogger("fortuna-orm")

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def select(self):
        pass

    def insert(self):
        pass

    def drop(self):
        pass

    def alter(self):
        pass

    def truncate(self):
        pass

    def describe(self):
        pass

    def show(self):
        pass

    def execute(self):
        pass

    def execute_many(self):
        pass

    def execute_script(self):
        pass

    def execute_file(self):
        pass

    def execute_sql(self):
        pass

    def execute_query(self):
        pass

    def execute_queries(self):
        pass

    def execute_transaction(self):
        pass

    def execute_transactions(self):
        pass

    def execute_procedure(self):
        pass

    def execute_function(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass

    def execute_table(self):
        pass

    def execute_schema(self):
        pass

    def execute_database(self):
        pass

    def execute_user(self):
        pass

    def execute_role(self):
        pass

    def execute_privilege(self):
        pass

    def execute_constraint(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass

    def execute_table(self):
        pass

    def execute_schema(self):
        pass

    def execute_database(self):
        pass

    def execute_user(self):
        pass

    def execute_role(self):
        pass

    def execute_privilege(self):
        pass

    def execute_constraint(self):
        pass

    def execute_trigger(self):
        pass

    def execute_event(self):
        pass

    def execute_view(self):
        pass

    def execute_index(self):
        pass

    def execute_sequence(self):
        pass
