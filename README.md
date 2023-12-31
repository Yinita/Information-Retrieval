# Information-Retrieval
This is a code repository for IR Homework by yinita (April-June 2023).

As you can see in there, there are 7 experiment example codes(include the final experiment). In the last few experiments, there are some sensitive data I would not give, so you may need to change it to your own accounts.

## Here is what every experiments did:

### Experiment 1, Task Purpose and Requirements:

#### Experimental purpose:

1. Master the establishment process of Inverted index;
2. Master the merging algorithm of inverted record tables;
3. Understand the simple invocation of Lucene's open source information retrieval library.
#### Experimental requirements:

1. Realize the establishment of Inverted index
2. Implementing Boolean retrieval algorithms

### Experiment 2, Task Purpose and Requirements:

#### Experimental purpose:

1. Master skip pointers technology, proximity search technology, Edit distance calculation method, pronunciation based correction technology, etc;
2. Understand the simple invocation of PorterStemmer open-source programs.

#### Experimental requirements:

1. Given a portion of the location index, please determine which documents match which queries
2. Implement an inverted record table merging algorithm based on skip table pointers, and verify the correctness of the algorithm on the example in Experiment 1.
3. Implement a merging algorithm for two inverted record tables in neighboring search, and make appropriate improvements according to requirements.
4. Implement Dynamic programming algorithm to calculate the Edit distance of two strings

### Experiment 3, Task Purpose and Requirements:

#### Experimental purpose: 

To master the statistical analysis methods of text datasets, as well as the construction and compression techniques of indexes.

#### Experimental requirements:

1. For the 593 documents in the attachment "HW3. txt" (each line represents a document with document IDs ranging from 1 to 593):
Use Chinese word segmentation tools (such as Jieba Chinese word segmentation) to segment text;
Count the total number of tokens and terms in 593 documents;
Build a Inverted index and output the queried document ID
2. Implement VB encoding and decoding
3. Implement encoding and decoding of Gamma codes

### Experiment 4, Task Purpose and Requirements:

#### Experimental purpose: 

master document scoring and probability based retrieval techniques such as Vector space model, BM25 and Language Model.

#### Experimental requirements:

1. Calculate the similarity values between 105 English documents in the attachment "HW4_1. txt" and return the 5 documents with the highest similarity for each document in documents 1-10 (if the similarity is the same, the document with the smaller document number will be returned first). It is required to use cosine similarity and TF-IDF to calculate the similarity between documents (keep two digits after the Decimal separator). English words are converted to lowercase without filtering or other conversion.



2. Calculate the similarity values between 593 Chinese documents in the attachment "HW4_2. txt" and return the 5 documents with the highest similarity for each document in documents 1-10 (if the similarity is the same, the document with the smaller document number will be returned first). It is required to use cosine similarity and TF-IDF to calculate the similarity between documents (two digits after the Decimal separator are reserved).

### Experiment 5, Task Purpose and Requirements:

#### Experimental purpose: 

To master the basic classification and clustering algorithms.

#### Experimental requirements:

1. Implementation of Feature selection method:
  (1) Implement Feature selection method based on Mutual information;
  (2) Realize the Feature selection method based on X ^ 2;
  (3) Use Chinese word segmentation tools to segment documents;
  (4) Use the 2022 news documents obtained from the school official document (a total of 200);
  (5) Using five categories as labels, select the 10 most relevant features for each category;

2. Implement naive Bayesian classification algorithm:
  (1) Implement a simple document classification system based on naive Bayesian classification algorithm;
  (2) Compare the classification effect of Feature selection and non Feature selection;
  (3) Train and test using the documents in question (1);

### Experiment 6, Task Purpose and Requirements:

#### Experimental purpose: 

To master classic link analysis algorithms such as PageRank and HITS.
 
#### Experimental requirements:

![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/0ebc47d9-a2b5-4a0d-93e6-679b33d693eb)

1. Implementation of PageRank algorithm
2. Calculate PageRank value manually

![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/6e377982-4aee-428a-a9c8-fb52a9311463)

3. HITS algorithm implementation


### final Experiment, Functions:

#### Basic functions:

1. Use open-source Chinese word segmentation programs (such as stuttering word segmentation) to segment Chinese sentences, and provide detailed instructions and configurations.

2. Use the open source English Stemming algorithm (such as the Porter algorithm) to process English documents and queries, and explain how to call related functions.

3. Develop an information retrieval system that supports user interaction, including input boxes and result displays (including hyperlinks), with a simple and aesthetically pleasing interface.

4. Use Inverted index to store data and analyze the Time complexity of Inverted index construction.

5. Use TF-IDF as the weight calculation method, provide Formula, explain the symbols and code implementation in the formula, and analyze Time complexity.

6. Use cosine similarity to calculate the correlation score of<query, document>, provide Formula, explain the symbols and code implementation in the formula, and analyze Time complexity.

7. Sort the matched documents based on the correlation score, return the top 10 results, and display the query time.

#### Featured features:

1. Real time update of system data, supporting large-scale data download or crawling.

2. Optimize the storage Space complexity of dictionary or inverted record table.

3. Support indexing news attachments.

4. Support displaying non textual content, such as images.

5. Support search function by domain, including news classification for different domains.

6. Provide friendly user interaction, such as font coloring in red, to help users understand the results.

7. Consider other factors besides cosine similarity to sort the results, such as timeliness.

8. Support query suggestions and provide candidate queries.

9. Support query and error correction, identify error terms and provide candidate queries.

10. Other functions that are considered distinctive should be clearly explained.
