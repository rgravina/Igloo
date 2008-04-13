import unittest, doctest
    
def suite():
    suite = unittest.TestSuite([
        doctest.DocFileTest('tagging.txt'),
        ])
    runner = unittest.TextTestRunner()
    runner.run(suite)
        
if __name__ == '__main__':
    suite()
