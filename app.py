import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Use 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, render_template_string

# --- (1) Mock Data Generation (Simulating Web Scraping) ---
# In a real app, you'd use 'requests' and 'BeautifulSoup' here.
# Example of real scraping (commented out):
# --------------------------------------------------------
# from bs4 import BeautifulSoup
# import requests
# 
# def scrape_ecommerce_site(url):
#     try:
#         response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#         response.raise_for_status() # Raise an error for bad responses
#         soup = BeautifulSoup(response.text, 'lxml')
#         
#         products = []
#         for item in soup.find_all('div', class_='product-item'): # Fictional class
#             title = item.find('h2', class_='product-title').text.strip()
#             price_str = item.find('span', class_='price').text.strip().replace('$', '').replace(',', '')
#             rating_str = item.find('div', class_='rating').text.strip().split('/')[0]
#             description = item.find('p', class_='description').text.strip()
#             
#             products.append({
#                 'title': title,
#                 'price': float(price_str),
#                 'rating': float(rating_str),
#                 'description': description,
#                 'category': 'Electronics' # You could try to find this too
#             })
#         return products
#     except Exception as e:
#         print(f"Error scraping {url}: {e}")
#         return []
# --------------------------------------------------------

def get_mock_product_data():
    """Returns a list of dictionaries, simulating scraped product data."""
    return [
        {'title': 'Pro-Grade Wireless Mouse', 'price': 89.99, 'rating': 4.7, 'description': 'Ergonomic wireless mouse with 8 programmable buttons and 16,000 DPI sensor.', 'category': 'Peripherals'},
        {'title': '4K Ultra-HD Monitor', 'price': 349.99, 'rating': 4.5, 'description': '27-inch IPS panel with 1ms response time and HDR support. Perfect for gaming and design.', 'category': 'Monitors'},
        {'title': 'Mechanical Keyboard (RGB)', 'price': 129.99, 'rating': 4.8, 'description': 'Full-size mechanical keyboard with custom blue switches and per-key RGB lighting.', 'category': 'Peripherals'},
        {'title': 'Noise-Cancelling Headphones', 'price': 249.50, 'rating': 4.6, 'description': 'Over-ear headphones with industry-leading active noise cancellation and 30-hour battery life.', 'category': 'Audio'},
        {'title': 'Portable SSD 1TB', 'price': 119.99, 'rating': 4.9, 'description': 'Blazing fast external SSD with read/write speeds up to 1,050 MB/s. USB-C compatible.', 'category': 'Storage'},
        {'title': 'Smartwatch Series 8', 'price': 399.00, 'rating': 4.4, 'description': 'Advanced health tracking, GPS, and a stunning always-on display.', 'category': 'Wearables'},
        {'title': 'Gaming Laptop 15-inch', 'price': 1499.99, 'rating': 4.3, 'description': 'High-performance gaming laptop with 12th-gen CPU and next-gen graphics card.', 'category': 'Computers'},
        {'title': 'Wireless Earbuds Pro', 'price': 199.99, 'rating': 4.7, 'description': 'True wireless earbuds with adaptive EQ, noise cancellation, and spatial audio.', 'category': 'Audio'},
    ]

# --- (2) Data Storage (Pandas DataFrame) ---
# Load the data into a pandas DataFrame on startup
df_products = pd.DataFrame(get_mock_product_data())

# --- (Optional) Save data to Excel ---
# You can uncomment the line below to save the initial data to an Excel file
# df_products.to_excel("scraped_products.xlsx", index=False)
# print("Data saved to scraped_products.xlsx")

# --- (3) Data Visualization ---
def create_visualization(data_df):
    """Creates a Seaborn plot and returns it as a base64 encoded string."""
    if data_df.empty:
        return ""
        
    try:
        # Calculate average price by category
        avg_price_df = data_df.groupby('category')['price'].mean().reset_index()
        
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid")
        # Create the bar plot
        ax = sns.barplot(
            x='category',
            y='price',
            data=avg_price_df,
            palette='viridis'
        )
        ax.set_title('Average Product Price by Category', fontsize=16)
        ax.set_xlabel('Category', fontsize=12)
        ax.set_ylabel('Average Price ($)', fontsize=12)
        
        # Save plot to a memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close() # Close the plot to free up memory
        
        # Encode buffer to base64
        data = base64.b64encode(buf.getbuffer()).decode('ascii')
        return f'data:image/png;base64,{data}'
    except Exception as e:
        print(f"Error creating visualization: {e}")
        return ""

# --- (4 & 5) Flask Web Application (UI & Search) ---
app = Flask(__name__)

# Define the HTML template as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Data</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                },
            },
        }
    </script>
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto max-w-7xl px-4 py-12">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">
            E-Commerce Product Dashboard
        </h1>

        <!-- Search Bar -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-8">
            <form method="POST" action="/" class="flex flex-col sm:flex-row gap-4">
                <input
                    type="text"
                    name="query"
                    placeholder="Search for products..."
                    value="{{ search_query }}"
                    class="flex-grow w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    class="bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-blue-700 transition duration-200"
                >
                    Search
                </button>
            </form>
        </div>

        <!-- Visualization -->
        <div class="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 class="text-2xl font-semibold text-gray-700 mb-4">
                Data Visualization
            </h2>
            {% if plot_base64 %}
                <img src="{{ plot_base64 }}" alt="Price by Category Chart" class="w-full h-auto">
            {% else %}
                <p class="text-gray-500">Could not load visualization.</p>
            {% endif %}
        </div>

        <!-- Product Listings -->
        <div>
            <h2 class="text-2xl font-semibold text-gray-700 mb-4">
                Product Listings
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {% if products %}
                    {% for product in products %}
                    <div class="bg-white rounded-lg shadow-md overflow-hidden transition-shadow duration-300 hover:shadow-xl">
                        <div class="p-6">
                            <h3 class="text-xl font-bold text-gray-800 mb-2">
                                {{ product.title }}
                            </h3>
                            <div class="flex justify-between items-center mb-3">
                                <span class="text-2xl font-bold text-green-600">
                                    ${{ "%.2f"|format(product.price) }}
                                </span>
                                <span class="px-3 py-1 bg-yellow-200 text-yellow-800 text-sm font-semibold rounded-full">
                                    Rating: {{ product.rating }}/5.0
                                </span>
                            </div>
                            <p class="text-gray-700">
                                {{ product.description }}
                            </p>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-gray-600 text-lg col-span-full text-center">
                        No products found matching your search.
                    </p>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    """Main page, handles search and displays data."""
    search_query = ""
    filtered_df = df_products

    # Handle search functionality
    if request.method == "POST":
        search_query = request.form.get("query", "").strip()
        if search_query:
            # Filter the DataFrame based on the query (case-insensitive)
            filtered_df = df_products[
                df_products['title'].str.contains(search_query, case=False) |
                df_products['description'].str.contains(search_query, case=False)
            ]

    # Generate the visualization
    # We plot all data, not just the filtered results
    plot_base64 = create_visualization(df_products)
    
    # Convert the filtered DataFrame to a list of dictionaries for the template
    products_list = filtered_df.to_dict('records')
    
    return render_template_string(
        HTML_TEMPLATE,
        products=products_list,
        plot_base64=plot_base64,
        search_query=search_query
    )

if __name__ == "__main__":
    app.run(debug=True)