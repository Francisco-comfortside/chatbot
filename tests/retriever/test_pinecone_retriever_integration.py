# test_retriever_integration.py
import unittest
from retriever.pinecone_retriever import retrieve_relevant_chunks, retrieve_direct

class TestRetrieveRelevantChunksIntegration(unittest.TestCase):
    # def test_retrieve_from_real_index(self):
    #     query = "What are the product dimensions of model CH-R24MOLVWM-230VI?"
    #     results = retrieve_relevant_chunks(query, k=1)
    #     self.assertTrue(len(results) > 0)
    #     print("Results:", results)

    # def test_retrieve_from_real_index_w_filter(self):
    #     query = "What are the product dimensions of model CH-R24MOLVWM-230VI?"
    #     results = retrieve_relevant_chunks(query, filters={"metadata.model_number": "CH-R24MOLVWM-230VI"}, k=1)
    #     self.assertTrue(len(results) > 0)
    #     print("Results:", results)

    def test_retrieve_direct_pinecone(self):
        query = "What are the product dimensions of model CH-R24MOLVWM-230VI?"
        results = retrieve_direct(query, k=1)
        print("Results:", results)
        self.assertTrue(len(results) > 0)

if __name__ == "__main__":
    unittest.main()

