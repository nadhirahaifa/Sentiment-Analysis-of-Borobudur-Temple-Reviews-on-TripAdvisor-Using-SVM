import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import operator
import os

# define the layout of the dashboard
st.set_page_config(layout="wide")

# load dataset
df_aspect = pd.read_csv(os.path.join(os.getcwd(), 'dataset/aspect_labelled.csv'))
df_dashboard = pd.read_csv(os.path.join(os.getcwd(), 'dataset/new_dashboard.csv'))
df_keywords = pd.read_excel(os.path.join(os.getcwd(), 'dataset/keywords.xlsx'))

# modified value in df_aspect['label'] column
df_aspect['label'] = df_aspect['label'].replace({1: 'positive', 0: 'neutral', -1: 'negative'})

# add the column label to df_dashboard
df_dashboard = pd.merge(df_dashboard, df_aspect[['text', 'label']], 
                        left_on='review', right_on='text', how='left')

# Drop the 'text' column from df_dashboard after the merge, as it is redundant
df_dashboard = df_dashboard.drop(columns=['text'])

# extract the date from the 'date_of_visit' column
df_dashboard['date_of_visit'] = pd.to_datetime(df_dashboard['date_of_visit'])
df_dashboard['date_of_visit'] = df_dashboard['date_of_visit'].dt.date

# extract the year
df_dashboard['year_of_visit'] = pd.DatetimeIndex(df_dashboard['date_of_visit']).year

aspect_colors = {
    'attraction': '#d90429', #red
    'image': '#70d6ff', #blue
    'human resource': '#000000', #black
    'amenities': '#FFC43D', #yellow
    'accessibility': '#f57a0f', #orange
    'price': '#52b788' #green
}

# count the number for each sentiment
def count_sentiment():
    labels = df_aspect['label'].value_counts()
    return labels['positive'], labels['neutral'], labels['negative']

def count_per_year(data):
    # count the number of data per year
    temp = pd.to_datetime(data).dt.year
    datas = temp.value_counts().reset_index()
    datas.columns = ['year', 'count']
    datas = datas.sort_values(by='year')
    return datas

def sentiment_per_time(data):
    df_sentiment = data.groupby(['year_of_visit', 'label'])['rating'].count().reset_index()
    df_sentiment.columns = ['Year', 'Sentiment', 'Count']

    # plot line chart
    fig = px.line(df_sentiment, x='Year', y='Count', color='Sentiment',
                labels={'Year': 'Year', 'Count': 'Number of Reviews', 'Sentiment': 'Sentiment'}, markers=True)
    return fig

def count_aspect_per_sentiment():
    attraction_counts = df_aspect[df_aspect['attraction'] == 1]['label'].value_counts().reset_index()
    amenities_counts = df_aspect[df_aspect['amenities'] == 1]['label'].value_counts().reset_index()
    accessibility_counts = df_aspect[df_aspect['accessibility'] == 1]['label'].value_counts().reset_index()
    image_counts = df_aspect[df_aspect['image'] == 1]['label'].value_counts().reset_index()
    price_counts = df_aspect[df_aspect['price'] == 1]['label'].value_counts().reset_index()
    human_resources_counts = df_aspect[df_aspect['human_resources'] == 1]['label'].value_counts().reset_index()

    df_aspect_counts = pd.DataFrame({
        'Sentiment': ['positive', 'neutral', 'negative'],
        'Attraction': attraction_counts['label'],
        'Amenities': amenities_counts['label'],
        'Accessibility': accessibility_counts['label'],
        'Image': image_counts['label'],
        'Price': price_counts['label'],
        'Human Resources': human_resources_counts['label']
    })

    df_melted = df_aspect_counts.melt(id_vars='Sentiment', var_name='Aspect', value_name='Count')
    return df_melted

def sentiment_per_rating(data):
    df_sentiment = data.groupby(['rating', 'label'])['review'].count().reset_index()
    df_sentiment.columns = ['Rating', 'Sentiment', 'Count']

    # plot line chart
    fig = px.line(df_sentiment, x='Rating', y='Count', color='Sentiment',
                # title='Rating per Sentiment',
                labels={'Rating': 'Rating', 'Count': 'Number of Reviews', 'Sentiment': 'Sentiment'}, markers=True)
    # add title

    return fig

def create_wordcloud1(sentiment):
    sentiment_dict = {row['word']: row[sentiment] for _, row in df_keywords.iterrows()}

    def color_func(word, **kwargs):
        aspect = df_keywords[df_keywords['word'] == word]['aspect'].values[0]
        return aspect_colors.get(aspect, '#000000')  # default to black if aspect not found

    # create the graphic
    wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=color_func).generate_from_frequencies(sentiment_dict)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Remove axes
    plt.tight_layout(pad=0)  # Remove padding
    # plt.title(f'{sentiment.capitalize()} Sentiment Word Cloud')

    # get the top 5 words
    sentiment_dict = sorted(sentiment_dict.items(), key=operator.itemgetter(1), reverse=True)
    return fig, sentiment_dict[:5]

def create_wf(data):
    word_freq_df = pd.DataFrame(data, columns=['word', 'frequency'])
    fig = px.bar(word_freq_df, x='frequency', y='word', color='word', 
                # title='Top 5 Positive Words',
                labels={'word': 'Word', 'frequency': 'Count'},
                text='frequency')
    # delete the legend
    fig.update_layout(showlegend=False)

    return fig

def main():
    st.header('Candi Borobudur Review Dashboard')
    
    # define the sentiment count
    pos, neu, neg = count_sentiment()

    # columns for scorecard
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label='Total Reviews', value=len(df_aspect), delta='')
    with col2:
        st.metric(label='Positive Reviews', value=pos, delta='')
    with col3:
        st.metric(label='Neutral Reviews', value=neu, delta='')
    with col4:
        st.metric(label='Negative Reviews', value=neg, delta='')
    with col5:
        st.metric(label='Average Rating', value=round(df_dashboard['rating'].mean(), 2), delta='')
    
    col1, col2 = st.columns(2)
    with col1:
        # chart of sentiment distribution
        st.subheader('Sentiment Distribution')
        fig = px.pie(df_aspect, names='label')
        st.plotly_chart(fig)
    with col2:
        # chart number of reviews per year
        st.subheader('Number of Reviews per Year')
        year_counts = count_per_year(df_dashboard['review_date'])
    
        # create the chart
        fig = px.line(year_counts, x='year', y='count',
                labels={'year': 'Year', 'count': 'Number of Review'},
                markers=True)
        st.plotly_chart(fig)

    # sentiment per year
    st.subheader('Sentiment per Year')
    fig = sentiment_per_time(df_dashboard)
    st.plotly_chart(fig)

    # sentiment counts per aspect
    st.subheader('Sentiment Counts per Aspect')
    df_per_aspect = count_aspect_per_sentiment()

    # Plot using Plotly Express
    fig = px.bar(df_per_aspect, x='Aspect', y='Count', color='Sentiment', text='Count',
                barmode='group',  # Group bars for each sentiment
                labels={'Aspect': 'Aspect', 'Count': 'Number of Review', 'Sentiment': 'Sentiment'})

    # Update layout for better readability if needed
    # fig.update_layout(title_x=0.5, title='Sentiment Counts per Aspect')
    st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    with col1:
        # rating distribution
        st.subheader('Rating Distribution')
        fig = px.histogram(df_dashboard, x='rating', nbins=5, 
                            # title= 'Rating Distribution',
                            labels={'rating': 'Rating', 'count': 'Number of Reviews'},
                            text_auto=True)
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig)
    with col2:
        # rating distribution
        st.subheader('Rating per Sentiment')
        fig = sentiment_per_rating(df_dashboard)
        st.plotly_chart(fig)

    # chart type of visit distribution
    st.subheader('Type of Visit Distribution')
    visit_without_nan = df_dashboard.dropna(subset=['type_of_visit'])
    fig = px.pie(visit_without_nan, names='type_of_visit')
    st.plotly_chart(fig)

    # wordcloud
    st.subheader('Word Cloud')

    # get the wordcloud and word_freq
    pos_fig, pos_wf = create_wordcloud1('positive')
    neg_fig, neg_wf = create_wordcloud1('negative')
    neu_fig, neu_wf = create_wordcloud1('neutral')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text('Positive')
        pos_fig
    with col2:
        st.text('Neutral')
        neu_fig
    with col3:
        st.text('Negative')
        neg_fig
    
    st.text("Word Cloud Color Legend:")
    st.text("Red: Attraction | Blue: Image | Black: Human Resource | Yellow: Amenities | Orange: Accessibility | Green: Price")

    # word frequency
    st.subheader('Word Frequency')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text('Positive')
        fig = create_wf(pos_wf)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.text('Neutral')
        fig = create_wf(neu_wf)
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.text('Negative')
        fig = create_wf(neg_wf)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()