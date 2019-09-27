#
# Pow Default Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest

# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform

MODELNAME = "pow_test_model"
class TestClass:
    @pytest.mark.notonosx
    @pytest.mark.run(order=1)
    @pytest.mark.minimal
    def test_server(self):
        """ test if server starts
            calls baseurl:port/test/12 
            must return 12.
            This test the server, routing and method dispatching
        """
        print(" .. Test if server works" )        
        from multiprocessing import Process
        import redmonty.server
        import requests
        import redmonty.config as cfg
        import time
        p = Process(target=redmonty.server.main)
        p.start()
        # wait for the process to start
        # see: https://stackoverflow.com/questions/57929895/python-multiprocessing-process-start-wait-for-process-to-be-started
        time.sleep(5)
        testurl=cfg.server_settings["protocol"] + cfg.server_settings["host"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  

        r = requests.get(testurl)
        p.terminate()
        assert int(r.text)==12
    
    @pytest.mark.run(order=2)
    @pytest.mark.minimal
    def test_sql_generate_model(self):
        """ test if sql model is generated"""
        print(" .. Test generate_model")
        import redmonty.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "sql", appname="redmonty")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/sql/" + MODELNAME + ".py"))

    @pytest.mark.run(order=3)
    @pytest.mark.minimal
    def test_sql_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        print(" .. Test model is correct type")
        from redmonty.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)
    
    @pytest.mark.run(order=4)
    def test_sql_dbsetup(self):
        """ test the setup of the alembic environment """
        print(" .. Test SQL: db_setup")
        import redmonty.init_sqldb_environment
        import os
        os.chdir("..")
        r = redmonty.init_sqldb_environment.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    @pytest.mark.run(order=5)
    def test_sql_migration(self):
        """ test the setup of the alembic environment 
            generate a migration
        """
        print(" .. Test SQL: generate_migration")
        import redmonty.generate_migration
        import os
        os.chdir("..")
        script = redmonty.generate_migration.generate_migration(message="pow_test")
        assert os.path.exists(os.path.normpath(script.path))
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    @pytest.mark.run(order=6)
    def test_sql_dbupdate(self):
        """ test the setup of the alembic environment 
            actually migrate the DB schema up
        """
        print(" .. Test SQL: update_db -d up")
        import redmonty.update_db
        import os, time
        ret = None
        os.chdir("..")
        time.sleep(1)
        try:
            ret = redmonty.update_db.migrate("up")
        except Exception as e:
            print(e)
            ret = True
        time.sleep(5)
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    @pytest.mark.run(order=7)
    def test_if_sql_model_validation_works(self):
        """ 
            check if validation works
        """ 
        print(" .. Test SQL: model.upsert() and model.find()")
        from redmonty.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert m.validate() == True
    
    @pytest.mark.run(order=8)
    def test_if_sql_model_validation_fails_successfully(self):
        """ 
            check if validation fails if type is wrong
        """ 
        print(" .. Test SQL: model.upsert() and model.find()")
        from redmonty.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        m.title="123456789123456789123456789123456789"
        assert m.validate() == False

    @pytest.mark.run(order=9)
    def test_sql_insert_and_find(self):
        """ based on test_generate_model. 
            Tests if a model can insert values in the DB 
            and can be found by title attribute.
        """ 
        print(" .. Test SQL: model.upsert() and model.find()")
        from redmonty.models.sql.pow_test_model import PowTestModel
        import os
        m = PowTestModel()
        m.title = "TestnamePowTestRunner"
        m.upsert()
        res=m.find(PowTestModel.title=="TestnamePowTestRunner")
        assert res.count()==1
        m.session.close()
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

    #
    # tinyDB tests
    #
    @pytest.mark.run(order=10)
    @pytest.mark.minimal
    def test_tinydb_generate_model(self):
        """ test if sql model is generated"""
        print(" .. Test tinyDB generate_model")
        import redmonty.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "tinydb", appname="redmonty")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/tinydb/" + MODELNAME + ".py"))

    @pytest.mark.run(order=11)
    @pytest.mark.minimal
    def test_if_tinydb_model_validation_works(self):
        """ 
            check if validation works
        """ 
        print(" .. Test SQL: model.upsert() and model.find()")
        from redmonty.models.tinydb.pow_test_model import PowTestModel
        m = PowTestModel()
        assert m.validate() == True
    
    @pytest.mark.run(order=12)
    @pytest.mark.minimal
    def test_if_tinydb_model_validation_fails_successfully(self):
        """ 
            check if validation fails if type is wrong
        """ 
        print(" .. Test SQL: model.upsert() and model.find()")
        from redmonty.models.tinydb.pow_test_model import PowTestModel
        m = PowTestModel()
        m.title="123456789123456789123456789123456789"
        assert m.validate() == False
    
    @pytest.mark.run(order=13)
    @pytest.mark.minimal
    def test_tinydb_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        print(" .. Test model tinyDB is correct type")
        from redmonty.models.tinydb.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)
    
    @pytest.mark.run(order=14)
    def test_tinydb_insert_and_find(self):
        """ based on test_generate_model. Tests if a model can insert values 
            and can be found back.
        """ 
        print(" .. Test tinyDB: model.upsert() and model.find()")
        from redmonty.models.tinydb.pow_test_model import PowTestModel
        import os
        m = PowTestModel()
        m.title = "TestnamePowTestRunner"
        m.upsert()
        res=m.find(m.Query.title=="TestnamePowTestRunner")
        assert res
        m.db.close()
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    
    print(55*"-")
    print(" running pow Tests on: " + sys.platform)
    print(" ... ")
    if sys.platform.startswith("darwin"):
        # osx
        ret = pytest.main(["-k-notonosx", "pow_tests.py"])
    else:
        ret = pytest.main(["pow_tests.py"])
    
    print(" Failures: " +str(ret))
    print(55*"-")
    

