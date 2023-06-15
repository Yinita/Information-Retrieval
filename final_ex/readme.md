# Using Streamlit as our search engine fore-end:
### results show:
As we enter ```"streamlit run .\main_page.py"``` in our terminal
![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/9eb9efc0-17fa-4d27-9a18-e0c16d5e26a0)

And we can see the search engine fore-end in your default browser:
![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/84a364aa-6966-4261-a724-fa9287a33150)

#### Official Document Communication show:

For example, we enter the query:```英国留学 机构```

![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/f721f046-7b21-46ba-9321-1c9460ff8684)

In the left side, there are the Distribution of Result Categories and Time Information.
Also,there are two types of time consuming information in the bottom left corner.

![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/3572eb04-9bcc-45fb-beed-6eafcd682512)

We can see the result have a strong correlation.

#### School Celebration:

An example:

![image](https://github.com/Yinita/Information-Retrieval/assets/59158324/0270e510-55d2-4194-9cc9-0fb88f02d5bb)


## Here is the main pipeline of what each part do!:
There are all CN version, if you got anything confused, Please send me a private message, I will be happy to answer ^^:

### How we give user a query-recall?:

![mermaid-diagram-2023-06-15-182031](https://github.com/Yinita/Information-Retrieval/assets/59158324/8fae4a10-9686-4ad9-9e61-35ffe6440a78)

### main search engine fore-end:

![mermaid-diagram-2023-06-15-142653](https://github.com/Yinita/Information-Retrieval/assets/59158324/ae95cc7c-ba5a-42be-8422-25d39869de49)

### Extract the data from the html:

![mermaid-diagram-2023-06-15-180956](https://github.com/Yinita/Information-Retrieval/assets/59158324/d3aa259c-adcb-43b2-968c-6da577513ec9)

### Establish Inverted index:

![mermaid-diagram-2023-06-15-174537](https://github.com/Yinita/Information-Retrieval/assets/59158324/2abdb0dc-b58b-4e4e-9485-cc2d296595a9)

### Cosine similarity calculation:

![mermaid-diagram-2023-06-15-142806](https://github.com/Yinita/Information-Retrieval/assets/59158324/338f0410-e932-4e5e-a515-cccadd41b89c)

