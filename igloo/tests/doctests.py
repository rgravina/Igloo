import unittest, doctest
    
def suite():
    suite = unittest.TestSuite()
#    suite.addTest(doctest.DocFileTest('tagging.txt'))
    suite.addTest(doctest.DocFileTest('content.txt'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
        
if __name__ == '__main__':
    suite()
