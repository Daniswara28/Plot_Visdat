import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, HoverTool, ColorBar
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# Page config
st.set_page_config(
    page_title="AI Predictions & Interactive Visualizations",
    page_icon="🤖",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('spotify_songs.csv')
    return df

# Load the data
df = load_data()

# Header
st.title("🤖 AI Predictions & Interactive Visualizations")
st.markdown("""
This page features interactive visualizations using Bokeh and AI predictions for song popularity based on audio features.
""")

# Sidebar for feature selection
st.sidebar.header("Feature Selection")
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
selected_features = st.sidebar.multiselect(
    "Select features for prediction:",
    features,
    default=['danceability', 'energy', 'valence']
)

# Interactive Bokeh Visualization 1: Feature Relationships
st.header("🎵 Interactive Feature Relationships")

# Create Bokeh visualization for selected features
if len(selected_features) >= 2:
    x_feature = st.selectbox("Select X-axis feature:", selected_features)
    y_feature = st.selectbox("Select Y-axis feature:", 
                            [f for f in selected_features if f != x_feature])
    
    source = ColumnDataSource(df)
    
    p = figure(width=800, height=400, title=f"{x_feature.title()} vs {y_feature.title()}",
              tools="pan,box_zoom,reset,save,wheel_zoom")
    
    # Add color mapping based on popularity
    mapper = linear_cmap(field_name='track_popularity', palette=Viridis256,
                        low=min(df['track_popularity']), high=max(df['track_popularity']))
    
    # Create scatter plot
    scatter = p.scatter(x_feature, y_feature, size=8, alpha=0.6,
                       color=mapper, source=source)
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ('Track', '@track_name'),
        ('Artist', '@track_artist'),
        ('Popularity', '@track_popularity'),
        (x_feature.title(), f'@{x_feature}'),
        (y_feature.title(), f'@{y_feature}')
    ])
    p.add_tools(hover)
    
    # Add color bar
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8,
                        location=(0,0), title='Popularity')
    p.add_layout(color_bar, 'right')
    
    # Style the plot
    p.xaxis.axis_label = x_feature.title()
    p.yaxis.axis_label = y_feature.title()
    p.grid.grid_line_color = 'gray'
    p.grid.grid_line_alpha = 0.1
    
    st.bokeh_chart(p, use_container_width=True)

# AI Prediction Model
st.header("🎯 Popularity Prediction Model")

if len(selected_features) > 0:
    # Prepare data for modeling
    X = df[selected_features]
    y = df['track_popularity']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    with st.spinner("Training Random Forest model..."):
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = rf_model.predict(X_test_scaled)
        
        # Calculate feature importance
        feature_importance = pd.DataFrame({
            'feature': selected_features,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Display feature importance
        st.subheader("Feature Importance")
        fig = px.bar(feature_importance, x='feature', y='importance',
                    title='Feature Importance in Predicting Song Popularity')
        st.plotly_chart(fig)
        
        # Interactive Prediction
        st.subheader("Try Predicting Song Popularity")
        st.markdown("Adjust the sliders to see how different feature values affect the predicted popularity.")
        
        # Create sliders for each feature
        user_input = {}
        for feature in selected_features:
            min_val = float(df[feature].min())
            max_val = float(df[feature].max())
            mean_val = float(df[feature].mean())
            user_input[feature] = st.slider(
                f"Select {feature}",
                min_value=min_val,
                max_value=max_val,
                value=mean_val,
                step=(max_val - min_val) / 100
            )
        
        # Make prediction with user input
        user_input_df = pd.DataFrame([user_input])
        user_input_scaled = scaler.transform(user_input_df)
        prediction = rf_model.predict(user_input_scaled)[0]
        
        # Display prediction
        st.metric(
            label="Predicted Popularity Score",
            value=f"{prediction:.1f}/100"
        )

else:
    st.warning("Please select at least one feature for prediction in the sidebar.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Created with ❤️ using Bokeh and Scikit-learn</p>
</div>
""", unsafe_allow_html=True) 