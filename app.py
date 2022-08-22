import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# main Page
st.title('Welcome to What\'s Chat Analyzer 👋 😃')
st.caption('Analyze What\'s App Chat in Second')
st.markdown("""
            With this Application we can analyze what\'s app chat\'s. 
            we can analyze both individuals and groups chat as well with the application
            """)

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)
    with st.expander("See explanation"):
        st.write("""
            This is your Data set looks like.
        """)

    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header('Total Media Message ')
            st.title(num_media_messages)
        with col4:
            st.header('Total Number of Links')
            st.title(num_links)

        # group level analysis only
        if selected_user == 'Overall':
            st.title('')
            st.title("Most Busy Users 🤕")
            st.title('')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            st.title('')
            with st.expander("See explanation"):
                st.write("""
                    This graph will show most busiest user in the group, 
                    their number of the highest message in the group.
                """)
            with col1:
                ax.bar(x.index, x.values, color=['black', 'red', 'green', 'blue', 'cyan'])
                # ax.pie(x.values,x.index)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Monthly timeline

        st.title('Monthly Timeline 📊')
        st.title('')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict which is the most busiest months of our groups.
            """)
        # daily timeline

        st.title('Daily Timeline 📈')
        st.title('')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict that one of best time user use groups with their 
                friends / family to have chit chat.
            """)
        # activity map

        st.title("Activity map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day 📉")
            st.title('')
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.title('')
            with st.expander("See explanation"):
                st.write("""
                    With this graph we can clearly predict that one of best Day\'s user use groups with their 
                    friends / family to have chit chat.
                """)

        with col2:
            st.header("Most busy Month 📊")
            st.title('')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.title('')
            with st.expander("See explanation"):
                st.write("""
                    With this graph we can clearly predict that one of best Month user use groups with their 
                    friends / family to have chit chat.
                """)

        # heatmap
        st.title("Weekly Activity map 🗺")
        st.title('')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict that one of best time user use groups with their 
                friends / family to have chit chat.
            """)
        # wordCloud

        st.title('')
        st.title('Word Cloud 😶‍🌫')
        st.title('')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict that what are those words that our member use too.
            """)

        # most Common Words
        st.title('')
        most_common_df = helper.most_common_word(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        st.title('Most Common Words 📈')
        st.title('')
        st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict that what are those most common use by our user.
            """)
        word = most_common_df.head()
        if selected_user != 'Overall':
            chatapp = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='chatapp'
            )
            mycursor = chatapp.cursor()
            firstname, lastname = selected_user.split(" ")
            mycursor.execute(f"update users set words='{word[0][0]}' where fname='{firstname}' and lname='{lastname}' ")
            chatapp.commit()
            mycursor.close()

        # st.dataframe(word)
        # print(word[0][0])
        # print(selected_user)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('')
        st.title('Emoji Analyser 👻')
        st.title('')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0])
            st.pyplot(fig)
            # ax.scatter(emoji_df[1],emoji_df[0])
            # st.pyplot(fig)
        st.title('')
        with st.expander("See explanation"):
            st.write("""
                With this graph we can clearly predict that what type of their age groups and 
                what their most used emojis.
            """)
