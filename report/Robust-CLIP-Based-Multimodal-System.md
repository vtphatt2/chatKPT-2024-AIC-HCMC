# Paper : Enhancing Video Retrieval with Robust CLIP-Based Multimodal System
Authors : 
- Minh-Dung Le-Quynh (Lazada Vietnam - Ho Chi Minh, Viet Nam)
- Anh-Tuan Nguyen (University of Science - Ho Chi Minh, Viet Nam)
- Anh-Tuan Quang-Hoang (Ford Motor - Los Angeles, United States)
- Van-Huy Dinh (HUTECH University - Ho Chi Minh, Viet Nam)
- Tien-Huy Nguyen (University of Information Technology - Ho Chi Minh, Viet Nam)
- Hoang-Bach Ngo (University of Science - Ho Chi Minh, Viet Nam)
- Minh-Hung An (FPT Telecom - Ho Chi Minh, Viet Nam)

**Citation** : Minh-Dung Le-Quynh, Anh-Tuan Nguyen, Anh-Tuan Quang-Hoang, Van-Huy Dinh, Tien-Huy Nguyen, Hoang-Bach Ngo, and Minh-Hung An. 2023. Enhancing Video Retrieval with Robust CLIP-Based Multimodal System. In Proceedings of the 12th International Symposium on Information and Communication Technology (SOICT '23). Association for Computing Machinery, New York, NY, USA, 972–979. https://doi.org/10.1145/3628797.3629011

# ABSTRACT

> "In the rapidly evolving landscape of multimedia data, the need for efficient content-based video retrieval has become increasingly vital. To tackle this challenge, we introduce an interactive video retrieval system designed to retrieve data from vast online video collections efficiently. Our solution encompasses rich textual to visual descriptions, advanced human detection capabilities, and a novel Sketch-Text retrieval mechanism, rendering the search process comprehensive and precise. At its core, the system leverages the Contrastive Language-Image Pretraining (CLIP) model, renowned for its proficiency in bridging the gap between visual and textual data. Our user-friendly web application allows users to create queries, explore top results, find similar images, preview short video clips, and select and export pertinent data, enhancing the effectiveness and accessibility of content-based video retrieval."

# INTRODUCTION

> "Content-based video retrieval, the task of retrieving video frames based on textual queries, has gained significant attention in recent years. The demand > from users is steadily increasing, requiring faster query speeds and reduced time to locate a specific frame within a vast collection of videos based on the provided textual query."

> "By learning from a vast collection of text-image pairs and minimizing the cosine similarity between the text and image embedding vectors, CLIP has proven to be particularly well-suited for retrieving videos based on textual queries. The advent of CLIP has opened up many possibilities for developing robust and powerful content-based video retrieval pipelines."

> "In this paper, we introduce our system, which harnesses the power of the CLIP model to extract abstract, content-rich features from the videos in the dataset. To further enhance the capabilities of the CLIP model, we’ve integrated various supporting models and techniques, including human detection and retrieval from sketches and text. To facilitate rapid and robust retrieval, we efficiently index these features using **Faiss**, a state-of-the-art similarity search library, in conjunction with our database systems." 

# FAISS (Facebook AI Similarity Search)
**Key features** : Supports Large Datasets, Efficient Similarity Search
- **Image Search**: Finding images similar to a given query image.Finding images similar to a given query image.
- **Text Embeddings**: Finding semantically similar text or document vectors.

Faiss is a powerful backend tool for similarity searches and clustering vectors, essential for high-performance vector operations. FiftyOne provides a front-end solution for dataset management and model evaluation in computer vision, offering visualization and dataset manipulation capabilities.

# VIDEO PREPROCESSING
TransNet is a deep learning model specifically designed for video shot boundary detection.
1. Utilize the Transnet model to transform long video sequences into a list of scenes. 
2. Employ FFmpeg, to extract three main keyframes for each scene using the formula $p_i \in \{s + (e - s) \times (0.5i - 0.5) \,|\, i = 1, 2, 3\}$ ($s$, $e$ represent the first and last frame positions of the scene)

# MULTIMODAL RETRIEVAL

Users can input text queries in a natural language format, enabling them to achieve their search objectives through a more intuitive and user-centric approach.

• All keyframes collected from videos are embedded into vec- tors to store features in Faiss before retrieval

• When users input a text description query, it is embedded using the CLIP model to create a text-embedding vector.

• After obtaining the text embedding from the query, we per- form a cosine similarity measure between the text embed- ding vector and all the keyframe embedding vectors stored in Faiss. The returned result consists of the closest vectors in Faiss, limited to a specified number based on the top-K closest vectors with the highest similarity score.

• To improve the performance of the embedding model, we utilize the latest large CLIP model, specifically the Vision Transformer pretrained at a 336-pixel resolution (ViT-L/14@336p).
