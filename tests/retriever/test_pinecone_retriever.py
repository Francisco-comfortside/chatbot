import unittest
from unittest.mock import patch, MagicMock
from retriever.pinecone_retriever import retrieve_relevant_chunks

class TestRetrieveRelevantChunks(unittest.TestCase):
    
    @patch("retriever.pinecone_retriever.vectorstore")
    def test_retrieve_relevant_chunks_returns_results(self, mock_vectorstore):
        # Arrange: Setup mock return value
        mock_result_1 = MagicMock()
        mock_result_1.page_content = "This is a test chunk."
        mock_result_2 = MagicMock()
        mock_result_2.page_content = "This is another chunk."

        mock_vectorstore.similarity_search.return_value = [mock_result_1, mock_result_2]

        # Act: Call the function with a test query and filters
        query = "Test query"
        filters = {"metadata.model_number": "123O"}
        result = retrieve_relevant_chunks(query, filters, k=2)

        # Assert: Check that the function returns correct content
        self.assertEqual(result, [
            "This is a test chunk.",
            "This is another chunk."
        ])

        mock_vectorstore.similarity_search.assert_called_once_with(
            query=query,
            k=2,
            filter=filters
        )

if __name__ == "__main__":
    unittest.main()