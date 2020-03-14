import sys
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from search import search
import time
import threading
import queue

class MainSearchWindow(QDialog):
    def __init__(self):
        super(MainSearchWindow, self).__init__()
        loadUi('gui.ui', self)
        self.setWindowTitle("Search Engine - Assignment 3")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.searcher = search()
        self.book = self.searcher.create_bookeeper("./FileOutput/bookkeeping.txt")
        self.url_file = self.searcher.load_urls("./FileOutput/urls.txt")

    def clicked(self):
        print('clicked')

    def on_pushButton_clicked(self):
        query = self.lineEdit.text()
        if query == "":
            sys.exit()
        qList = self.searcher.readSearchQuery(query)
        starttime = time.time()
        if len(qList) == 0:
            string = "No valid query tokens. Could not find any results. Try again."
            model = QStandardItemModel(self.URLlabels)
            item = QStandardItem(string)
            item.setText(string)
            model.appendRow(item)

        que = queue.Queue()
        thread_list = []
        for word in qList:
            thread = threading.Thread(target=self.searcher.final_search_file,
                                      args=(self.book, "./FileOutput/finalmerged.txt", word, que))
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

        thread_list.clear()

        query_word_posting = []
        query_doc_setlist = []
        while not que.empty():
            posting = que.get()
            # print("posting: ",posting)
            # print(posting)
            query_word_posting.append(posting[0])
            query_doc_setlist.append(posting[1])
        # query_doc_setlist = intersect_sets(query_doc_setlist,posting[1])

        if len(query_word_posting) == 0:
            string = ("No valid tokens, please try again")
            model = QStandardItemModel(self.URLlabels)
            item = QStandardItem(string)
            item.setText(string)
            model.appendRow(item)


        merged_doc_set = self.searcher.add_dups(query_doc_setlist)

        cosine_vector = self.searcher.calculate_tfidf_cosine(query_word_posting)
        # print(len(query_word_posting))

        cosine_vector_keys = set(int(i) for i in cosine_vector.keys())
        final_doc_set = merged_doc_set.intersection(cosine_vector_keys)
        new_cos_vector = dict()
        for id in final_doc_set:
            new_cos_vector[id] = cosine_vector[str(id)]

        d = self.searcher.sort_my_dict(new_cos_vector, 5)
        URL = self.searcher.findURL(d, self.url_file)
        endtime = time.time() - starttime
        total_time = "Total Time Elapsed = " + str(endtime)

        search_results = "************  SEARCH RESULTS   *************"

        model = QStandardItemModel(self.URLlabels)
        item = QStandardItem(total_time)
        item.setText(total_time)
        model.appendRow(item)
        item = QStandardItem(search_results)
        item.setText(search_results)
        model.appendRow(item)
        for u in URL:
            # Create an item with a url
            item = QStandardItem(u)
            item.setText(u)
            model.appendRow(item)
        #model.setOpenExternalLinks(True)
        self.URLlabels.setModel(model)
        self.URLlabels.show()

app = QApplication(sys.argv)
window = MainSearchWindow()
window.show()
sys.exit(app.exec_())