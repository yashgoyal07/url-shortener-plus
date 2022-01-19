from app.controllers.mysql_controller import MysqlController
from app.helpers.mysql_queries import db_exist, customers_table_exist, links_table_exist



class TestDatabase:
    mysql_controller_obj = MysqlController()

    def test_db_connection(self):
        """
        Assert that Database connection is being made successfully.    
        """
        try:
            self.mysql_controller_obj.get_connection()
        except Exception as err:
            assert False, f"{err}"
    
    def test_db_present(self):
        """
        Assert that the database is created successfully.    
        """
        result = self.mysql_controller_obj.dql_query(query=db_exist)
        assert result != []

    def test_customers_table_present(self):
        """
        Assert that the customers table is created successfully.    
        """
        result = self.mysql_controller_obj.dql_query(query=customers_table_exist)
        assert result != []

    def test_links_table_present(self):
        """
        Assert that the links table is created successfully.    
        """
        result = self.mysql_controller_obj.dql_query(query=links_table_exist)
        assert result != []
    

