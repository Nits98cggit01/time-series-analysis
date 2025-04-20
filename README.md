<a id="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Deloitte Senior Data Analyst - Assignment</h3>

  <p align="center">
    Analyze and visualize post engagement behavior across different organization types (Traffic, E-Commerce) using post/comment timestamps and interaction metrics like likes and comment patterns. This application enables you to derive meaningful insights from public page activities and present them through bucketed activity plots and word clouds.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#folder-structure">Folder structure</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project performs the following analytical tasks:

* Extracts and cleans timestamped post and comment data
* Buckets engagement into 15-minute intervals for analysis
* Visualizes activity patterns for Traffic and E-Commerce pages
* Calculates average likes per post category
* Generates word clouds for each organization :smile:

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [[Python]]
* [[Pandas]]
* [[Matplotlib]]
* [[Openpyxl]]
* [[Wordcloud]]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Folder structure
  ```sh
    .
    ├── bucket_count/                               # Stores all Excel outputs required for plotting graphs for Exercise 1 and 2 (bucket counts)
    ├── Exercise output/                            # Contains all generated plots
    ├── wordclouds_by_organization/                 # Contains word clouds for each page - Result for Exercise 3.2
    ├── analysis.py/                                # Script for getting the high level analysis required for documentation purpose (Exploratory and document purpose only)
    ├── average_likes_per_category.xlsx/            # Output excel for Exercise 3.1
    ├── Comments.xlsx                               # Input dataset (comments)
    ├── Facebook engagement analysis report.docx    # Exercise 5 - Writeup
    ├── Facebook engagement analysis report.pptx    # Exercise 4 - Presentation on the assignment and insights
    ├── Post Summary.xlsx                           # Input dataset (posts)
    ├── test.ipynb                                  # Jupyter notebook for a quick feasibility check
    ├── tsa_fb_post_engagement.py                   # Core script with all analytics functions for the assignment (Exercise 1,2,3.1,3.2)
  ```

### Prerequisites

* Python 3.10+
* pip

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/yourusername/facebook-engagement-analysis.git
   cd facebook-engagement-analysis
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Add your data files:

* Post Summary.xlsx (must include createdTime, postedBy, category, likesCount, message, pid)
* Comments.xlsx (must include pid, commentsText)

2. Run the script
  ```sh
   python tsa_fb_post_engagement.py
   ```

3. Outputs
  * bucket_count/                   : This folder contains the excel sheets with the bucket count required for plotting the graphs
  * Exercise output/                : This folder contains the plot images for exercise 1 and exercise 2
  * average_likes_per_category.xlsx : output for exercise 3.1
  * wordclouds_by_organization/     : This folder contains the wordcloud images for each category - output for Exercise 3.2


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

* Add traffic page engagement analysis
* Add e-commerce comment analysis
* Plot posting behavior in 15-min buckets
* Calculate and export average likes per category
* Generate word clouds for each organization
* Add CLI options for filtering by date or page
* Dashboard with interactive graphs using Streamlit or Plotly
* Support for JSON/CSV input

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Made with ❤️ by Sreema K R
🔗 Email: sreemakumar2000@gmail.com
📁 GitHub: @yourusername

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sreema-k-r-760361265/
[Python]: https://www.python.org/
[Pandas]: https://pypi.org/project/pandas/
[Matplotlib]: https://pypi.org/project/matplotlib/
[Openpyxl]: https://pypi.org/project/openpyxl/
[Wordcloud]: https://pypi.org/project/wordcloud/
