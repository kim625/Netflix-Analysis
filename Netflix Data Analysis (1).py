#!/usr/bin/env python
# coding: utf-8

# ## Netflix Data Analysis Project

# Netflix is one of the largest streaming platforms nowadays. In this project, I analyzed their dataset of movies and TV shows using Python Pandas, Seaborn, and Matplotlib. After this analysis, we will gain a better understanding of the platform and derive meaningful insights from the data through visualized graphs.

# ## Data Preparation and Cleaning

# Before we delve into the analysis, let's take a peek at the dataset we will be working with. This initial exploration will allow us to familiarize ourselves with the data and understand what lies ahead.

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import seaborn as sns


# In[2]:


data = pd.read_csv("C:\\Users\\Seohyun Kim\\OneDrive\\Desktop\\DA project\\Netflix\\8. Netflix Dataset.csv")


# In[8]:


data.head(3)


# In[14]:


data.size


# In[16]:


data.dtypes


# In[18]:


data.info()


# ## Removing duplicates

# In[6]:


data[data.duplicated()]


# In[7]:


data.drop_duplicates(inplace = True)


# By using "inplace = True" line, make the change last permanently in the data set.

# In[27]:


data[data.duplicated]


# In[8]:


data.shape


# Make sure that the duplicated values are removed

# ## Show null value with heat map

# After removing duplicated data, our next step involved examining the presence of null values within the dataset. This crucial analysis allows us to identify any missing or incomplete data points, enabling us to address them effectively before further processing.

# ### isnull

# In[32]:


data.head()


# In[34]:


data.isnull()


# In[35]:


data.isnull().sum()


# In[10]:


sns.heatmap(data.isnull())
plt.title('Null value with heat map')


# This will show null values count thoroughout the data set.

# # Q&A and Visualization: Let's dig deeper!

# ## Q1. For"House of cards", what is the show ID and who is the director of this show?

# In[41]:


data[data['Title'].isin(['House of Cards'])]


# Another way to find certain data is by using the "str.contains" function.

# In[44]:


data[data['Title'].str.contains('House of Cards')]


# ## Q2. In which year the highest number of movies and TV shows were released? w/ Bar graph

# In[46]:


data.dtypes


# In[48]:


data['Date_N'] = pd.to_datetime(data['Release_Date'])


# In[50]:


data['Date_N'].dt.year.value_counts()


# In[52]:


data['Date_N'].dt.year.value_counts().plot(kind='bar')


# In this dataset, we can observe that the year with the most content is 2019. The number of movies and TV shows on Netflix has been steadily increasing until 2019, but there was a decrease in content in 2020. It's important to note that this decline might be due to the COVID-19 pandemic, which likely affected the production and availability of new content during that year.

# ## Q3. How many movies & TV shows are in this data set?

# In[54]:


data.groupby('Category').Category.count()


# In[61]:


sns.countplot(x=data['Category'])
plt.title("Number of Movies and TV Shows")
plt.xlabel("Movies/TV Shows")
plt.ylabel("Total Count")


# The dataset consists of over 2,000 TV shows and 5,000 movies. It is evident that the number of movies is twice that of TV shows.

# ## Q4. Show all the movies that were released in 2020

# In[67]:


data[(data['Category']=='Movie') & (data['Year'] == 2020)]


# ### Number of Movies and TV Shows each year

# In[68]:


plt.figure(figsize =(12,6))
sns.countplot(data=data, x = "Year", hue = "Category")
plt.title("Number of Movies and TV Shows each year")


# Each year, the dataset consistently exhibits a higher count of movies compared to TV shows. Since 2016, there has been a significant and continuous growth in the quantity of both types of content until 2019. Notably, the number of TV shows has shown consistent growth over the years, up until 2020.

# ## Q5. Show only the Title of all TV shows that were released in United States only

# In[18]:


data[(data['Category'] == 'TV Show') & (data['Country'] == 'United States')]['Title']


# ## Q6. Top 15 countries on Netlfix based on amount of content

# In[13]:


filtered_countries = data.set_index('Category').Country.str.split(',', expand=True)
filtered_countries = filtered_countries[filtered_countries.notnull()]
filtered_countries.head()

plt.figure(figsize=(12,6))
sns.countplot(y = filtered_countries[0], order = filtered_countries[0].value_counts().index[:15])
plt.title('Top 15 Countries on Netflix')
plt.xlabel('Category')
plt.ylabel('Country')
plt.show()


# The United States has the most content on Netflix, followed by India in second place and the United Kingdom in third place. There is a considerable gap between the number of content offerings from the U.S. and India. The U.S. has over 2500 content items, while India has 900+ content items in second place. This highlights the dominance of U.S. content on Netflix when it comes to quantity. There are several Asian countries that rank prominently. This indicates a growing trend of anime and K-drama on Netflix, reflecting their popularity among viewers.

# ## Q7. Show Top 10 Directors who gave the highest number of Tv shows & Movies to Netflix

# In[16]:


movie_directors =data.groupby('Director')[['Title']].count().sort_values(by=['Title'], ascending=False).head(10)
movie_directors = movie_directors.reset_index()

movie_directors.rename(columns={'Title': 'Number of Movies'}, inplace = False)


# ## Q8. Show all the Records, where "Category is TV Show and Type is British TV Shows" or "Country is United Kingdom".

# In[4]:


data[(data['Category'] == 'TV Show') & (data['Type'] == 'British TV Shows') | (data['Country'] == 'United Kingdom')]


# ## Q9. In how many movies/shows, Tom Cruise was cast ?

# In[94]:


data[data['Cast'] == 'Tom Cruise']


# The filtering didn't work bc this can't process the columns with multiple elements. We have to create new data frame w/ dropna() function. I used the dropna() function to drop the rows that contain missing values. This helped me to find the shows that have Tom Cruise without having an error.

# In[95]:


new_data = data.dropna()
new_data[new_data['Cast'].str.contains('Tom Cruise')]


# ## Q10. What are the different Ratings defined by Netflix ?

# In[97]:


data['Rating'].unique()


# In[99]:


data['Rating'].nunique()


# In[11]:


order = 'G', 'TV-Y', 'TV-G', 'PG', 'TV-Y7', 'TV-Y7-FV', 'TV-PG', 'PG-13', 'TV-14', 'R', 'NC-17', 'TV-MA'
plt.figure(figsize = (12,6))
sns.countplot(x = data.Rating, hue = data.Category, order = order)
plt.title('Ratings for Movies and TV Shows')
plt.xlabel('Rating')
plt.ylabel('Total Count')
plt.show()


# We didn't include the ratings NR and UR in the visual since they stand for unrated and non-rated content. For both TV shows and movies, the most common rating on Netflix is "TV-MA". This indicates that there is a higher proportion of content targeted towards mature audiences rather than younger viewers.

# ### Q10-(1). How many TV Shows got the 'R' rating, after year 2018 ?

# In[102]:


data[(data['Category'] == 'TV Show') & (data['Rating'] == 'R') & (data['Year'] > 2018)].shape


# ## Q11. What is the maximum duration of a Movie/Show on Netflix ?

# In[103]:


data['Duration'].unique()


# In[104]:


data.Duration.dtypes


# Duration data is an object format so we have to format it as integer to find the maximum duration.

# In[106]:


data[['Minute','Unit']] = data['Duration'].str.split(' ', expand =True)


# In[108]:


data.head(2)


# In[110]:


data['Minute'] = pd.to_numeric(data['Minute'])


# In[111]:


data['Minute'].max()


# As an initial step, we converted the duration data type to numeric values. This allowed us to analyze the content duration more effectively. By separating the duration into minutes and units, we discovered that the longest content on Netflix has a duration of 312 minutes.

# ## Q12. Which individual country has the Highest No. of TV Shows ?

# In[113]:


data_tvshow = data[data['Category'] == 'TV Show']


# In[115]:


data_tvshow.head()


# In[116]:


data_tvshow.Country.value_counts().head(1)


# Based on the visual representation of the "Top 15 Countries on Netflix," it is evident that the United States has the highest number of TV shows, as they occupy the first position in the graph.

# ## Q13. How can we sort the dataset by Year ?

# In[117]:


data.sort_values(by='Year', ascending = False).head()


# ## Q14. Count all the instances where: Category is 'Movie' and Type is 'Dramas' or Category is 'TV Show' & Type is 'Kids' TV'.

# In[12]:


data[(data['Category'] ==  'Movie') & (data['Type'] == 'Dramas') | (data['Category'] ==  'TV Show') & (data['Type'] == "Kids' TV")].shape


# # Conclusions and Insights

# * The number of movies and TV shows on Netflix has been steadily increasing until 2019, but there was a decrease in content in 2020. This decline might be due to the COVID-19 pandemic, which likely affected the production and availability of new content during that year.
# 
# * The dataset consists of a total of 7,787 content items, with 5,377 movies and 2,410 TV shows. Each year, the dataset consistently exhibits a higher count of movies compared to TV shows.
# 
# * Since 2016, there has been significant and continuous growth in the quantity of both types of content until 2019. Notably, the number of TV shows has shown consistent growth over the years, up until 2020.
# 
# * The United States has the most content on Netflix, followed by India in second place and the United Kingdom in third place. In terms of quantity, the United States takes the lead on Netflix with over 2,500 content items, emphasizing its dominant position. In contrast, India secures second place with 900+ content items, indicating a significant gap between the two countries when it comes to the number of content on Netflix.
# 
# * There are several Asian countries that rank prominently. This indicates a growing trend of anime and K-drama on Netflix, reflecting their popularity among viewers.
# 
# * The most common rating on Netflix is "TV-MA". This indicates that there is a higher proportion of content targeted toward mature audiences rather than younger viewers.
# 
# * We discovered that the longest content on Netflix has a duration of 312 minutes.
# * The majority of null values in the dataset are found in the Director column.
# 
# * The United States has the highest number of TV shows, as they occupy the first position in the "Top 15 Countries on Netlfix" graph.

# # References

# Project - 8 | Data Analysis with Python | #DataScience | Netflix Dataset
# https://www.youtube.com/watch?v=b7Kd0fLwgO4
# 
# Jovian Netflix Data Analysis
# https://jovian.com/smartyshub5/netflix-data-analysis
