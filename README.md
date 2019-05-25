# git-RecommenderSystem

This project deals with the question of how one can implement a simple recommender
 system for an e-commerce online shop. We investigate this question by building a 
two-sided interface: from one side, the business owner can adjust the model to fit 
the specific business situation and from the other side, the customer receives product 
recommendations for a chosen product. To show the practicality of this interface we 
follow in the footsteps of a manager who wants to make a simple recommender system 
for the the sales of Amazon products. Thus, we use the official Amazon product data set.

## Getting Started

Use the following command to download the project.
```
git clone https://github.com/azommerf/git-RecommenderSystem.git
```

### Prerequisites

For this project you will first need to install any version of Python 3 (https://www.python.org/). 
Then, the following python toolboxes are needed: flask, sklearn, pandas and numpy. We provide a 
requirements.txt file in the repository to make installation easier. From the git-RecommenderSystem 
directory you can run the following command.
```
pip install -r ./requirements.txt
```

### Installing

Installing the program is just as easy as cloning the git repository into your local computer. 
After having the prerequisites installed, you go into the git-RecommenderSystem directory and 
run the following command.

```
python -m program
```

That's it! It might take 10 to 30 seconds to start the Flask web application.

## Running the program

As stated before, from the git-RecommenderSystem directory on you can run the following command 
to start the application.
```
python -m program
```

Your standard browser will automatically open a new tab with the web interface which directs 
you to the home page. Now you can start the process of the recommender system. Please refer 
to the flowchart inside the documentation folder to get a better understanding of what the 
program is doing. From the home page you can click to the next page which will lead you to a 
3-step process to prepare the recommender system. First, you download the selected database 
(warning, this might take a few minutes - please check the download status at your terminal). 
Second, you prepare the pandas DataFrame for further computations. Third, you convert this 
DataFrame into a CSR matrix. Now you are ready to continue to the recommender algorithm in 
the next page. Here you can set different KNN algorithms and change the underlying distance metric. 
We find that the best results for the Amazon data set is given with algorithm set to 'auto' 
along with a cosine distance metric. Test it for yourself! Finally, please watch the guidelines 
for the product identification and do keep in mind that the Amazon Simple Storage Service data set
is not (!) completely synchronized with the actual offered products (which unfortunately leads too 
often to the "product not identified" message). We are open for suggestions to make this program better!

## References

Please check the documentation for the "Reference List.pdf" and "Project Report.pdf" for all 
the references used for the development of the project.

## Authors

* Alvaro Morales
* Pascal Schenk
* André Zommerfelds
