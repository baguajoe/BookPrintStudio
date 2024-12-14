import React from "react";
import { Link } from "react-router-dom";

const Products = () => {
  return (
    <div>
      <h1>Products</h1>
      <ul>
        <li>
          <Link to="/products/all">All Products</Link>
        </li>
        <li>
          <Link to="/products/books">Books</Link>
        </li>
        <li>
          <Link to="/products/ebooks">eBooks</Link>
        </li>
        <li>
          <Link to="/products/audiobooks">Audiobooks</Link>
        </li>
        <li>
          <Link to="/products/comic-books">Comic Books</Link>
        </li>
        <li>
          <Link to="/products/tshirts">T-Shirts</Link>
        </li>
      </ul>
    </div>
  );
};

export default Products;
