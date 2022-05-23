from unittest import TestCase, main
from db import *

class Test(TestCase):
    def test_results(self):
        print("initial: ", get_keywords(), get_results("test"))
        add_result("test", [{
            'title': "title",
            'company': "company",
            'location': "location",
            'time': "time",
            'link': "link"
        }])
        print("add: ", get_keywords(), get_results("test"))
        delete_result("test")
        print("delete: ", get_keywords(), get_results("test"))

if __name__ == "__main__":
    main()