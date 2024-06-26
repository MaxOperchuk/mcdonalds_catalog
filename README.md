# McDonald's Menu API

This API provides access to the McDonald's menu items along with their nutritional information.

## Getting Started

To get started with this API, follow the instructions below.

### Prerequisites

Make sure you have Python installed on your system. You will also need to install the required libraries listed in the `requirements.txt` file.
If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
```bash
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

### Usage

Run the API server using the following command:

```bash
python -m uvicorn main:app --reload
```

#### Endpoints

The API provides the following endpoints:

- GET /all_products/ 
Returns all information about all products in the McDonald's menu.
````
http://localhost:8000/all_products/
````

- GET /products/{product_name}
Returns information about the exact product specified by its name.
````
http://localhost:8000/products/Американо
````

- GET /products/{product_name}/{product_field}
Returns information about the exact field of the specified product.
````
http://localhost:8000/products/Американо/name
````
