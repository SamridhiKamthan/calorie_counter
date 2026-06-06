import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# ================= DATABASE SETUP =================

DB_NAME = "calorie_tracker.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        calorie_goal INTEGER DEFAULT 2000,
        protein_goal INTEGER DEFAULT 150,
        carb_goal INTEGER DEFAULT 250,
        fat_goal INTEGER DEFAULT 65,
        water_goal INTEGER DEFAULT 8,
        weight REAL DEFAULT 70,
        height REAL DEFAULT 170,
        age INTEGER DEFAULT 25,
        gender TEXT DEFAULT 'Male',
        activity_level TEXT DEFAULT 'Moderately Active'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        food_name TEXT,
        calories INTEGER,
        protein REAL DEFAULT 0,
        carbs REAL DEFAULT 0,
        fat REAL DEFAULT 0,
        serving_size TEXT,
        meal_type TEXT DEFAULT 'Other',
        log_date TEXT,
        log_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        glasses INTEGER,
        log_date TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()

# ================= COMPREHENSIVE FOOD DATABASE =================

food_database = {
    # -- Fruits --
    "Apple (1 medium, 182g)":           {"cal": 95,  "protein": 0.5, "carbs": 25.1, "fat": 0.3, "category": "Fruits"},
    "Banana (1 medium, 118g)":          {"cal": 105, "protein": 1.3, "carbs": 27.0, "fat": 0.4, "category": "Fruits"},
    "Orange (1 medium, 131g)":          {"cal": 62,  "protein": 1.2, "carbs": 15.4, "fat": 0.2, "category": "Fruits"},
    "Mango (1 cup, 165g)":             {"cal": 99,  "protein": 1.4, "carbs": 24.7, "fat": 0.6, "category": "Fruits"},
    "Grapes (1 cup, 151g)":            {"cal": 104, "protein": 1.1, "carbs": 27.3, "fat": 0.2, "category": "Fruits"},
    "Watermelon (1 cup, 152g)":        {"cal": 46,  "protein": 0.9, "carbs": 11.5, "fat": 0.2, "category": "Fruits"},
    "Strawberries (1 cup, 152g)":      {"cal": 49,  "protein": 1.0, "carbs": 11.7, "fat": 0.5, "category": "Fruits"},
    "Pineapple (1 cup, 165g)":         {"cal": 82,  "protein": 0.9, "carbs": 21.6, "fat": 0.2, "category": "Fruits"},
    "Papaya (1 cup, 145g)":            {"cal": 62,  "protein": 0.7, "carbs": 15.8, "fat": 0.4, "category": "Fruits"},
    "Pomegranate (1 medium, 282g)":    {"cal": 234, "protein": 4.7, "carbs": 52.7, "fat": 3.3, "category": "Fruits"},
    "Kiwi (1 medium, 69g)":            {"cal": 42,  "protein": 0.8, "carbs": 10.1, "fat": 0.4, "category": "Fruits"},
    "Guava (1 medium, 55g)":           {"cal": 37,  "protein": 1.4, "carbs": 7.9,  "fat": 0.5, "category": "Fruits"},
    "Blueberries (1 cup, 148g)":       {"cal": 84,  "protein": 1.1, "carbs": 21.4, "fat": 0.5, "category": "Fruits"},
    "Avocado (1 medium, 150g)":        {"cal": 240, "protein": 3.0, "carbs": 12.8, "fat": 22.0, "category": "Fruits"},
    "Jackfruit (1 cup, 165g)":         {"cal": 156, "protein": 2.8, "carbs": 38.4, "fat": 1.1, "category": "Fruits"},
    "Lychee (1 cup, 190g)":            {"cal": 125, "protein": 1.6, "carbs": 31.4, "fat": 0.8, "category": "Fruits"},

    # -- Vegetables --
    "Spinach (1 cup cooked, 180g)":     {"cal": 41,  "protein": 5.3, "carbs": 6.8,  "fat": 0.5, "category": "Vegetables"},
    "Broccoli (1 cup, 156g)":           {"cal": 55,  "protein": 3.7, "carbs": 11.2, "fat": 0.6, "category": "Vegetables"},
    "Carrot (1 medium, 61g)":           {"cal": 25,  "protein": 0.6, "carbs": 5.8,  "fat": 0.1, "category": "Vegetables"},
    "Potato (1 medium, 148g)":          {"cal": 163, "protein": 4.3, "carbs": 37.0, "fat": 0.2, "category": "Vegetables"},
    "Sweet Potato (1 medium, 114g)":    {"cal": 103, "protein": 2.3, "carbs": 24.0, "fat": 0.1, "category": "Vegetables"},
    "Tomato (1 medium, 123g)":          {"cal": 22,  "protein": 1.1, "carbs": 4.8,  "fat": 0.2, "category": "Vegetables"},
    "Cucumber (1 cup sliced, 120g)":    {"cal": 16,  "protein": 0.7, "carbs": 3.8,  "fat": 0.1, "category": "Vegetables"},
    "Onion (1 medium, 110g)":           {"cal": 44,  "protein": 1.2, "carbs": 10.3, "fat": 0.1, "category": "Vegetables"},
    "Cauliflower (1 cup, 107g)":        {"cal": 27,  "protein": 2.1, "carbs": 5.3,  "fat": 0.3, "category": "Vegetables"},
    "Green Peas (1 cup, 160g)":         {"cal": 125, "protein": 8.6, "carbs": 22.5, "fat": 0.6, "category": "Vegetables"},
    "Capsicum (1 medium, 119g)":        {"cal": 31,  "protein": 1.0, "carbs": 6.0,  "fat": 0.3, "category": "Vegetables"},
    "Cabbage (1 cup, 89g)":             {"cal": 22,  "protein": 1.1, "carbs": 5.2,  "fat": 0.1, "category": "Vegetables"},
    "Lady Finger / Okra (1 cup, 100g)": {"cal": 33,  "protein": 1.9, "carbs": 7.0,  "fat": 0.2, "category": "Vegetables"},
    "Bottle Gourd (1 cup, 116g)":       {"cal": 19,  "protein": 0.6, "carbs": 4.5,  "fat": 0.1, "category": "Vegetables"},
    "Beetroot (1 cup, 136g)":           {"cal": 58,  "protein": 2.2, "carbs": 13.0, "fat": 0.2, "category": "Vegetables"},
    "Corn (1 ear, medium, 100g)":       {"cal": 90,  "protein": 3.3, "carbs": 19.0, "fat": 1.2, "category": "Vegetables"},
    "Mushroom (1 cup, 70g)":            {"cal": 15,  "protein": 2.2, "carbs": 2.3,  "fat": 0.2, "category": "Vegetables"},

    # -- Indian Breads & Staples --
    "Roti / Chapati (1 medium, 45g)":    {"cal": 120, "protein": 3.6, "carbs": 20.0, "fat": 2.5, "category": "Indian Staples"},
    "Naan (1 piece, 90g)":               {"cal": 262, "protein": 8.7, "carbs": 45.0, "fat": 5.1, "category": "Indian Staples"},
    "Paratha (1 medium, 80g)":           {"cal": 250, "protein": 5.0, "carbs": 35.0, "fat": 10.0, "category": "Indian Staples"},
    "Puri (1 piece, 40g)":               {"cal": 150, "protein": 2.8, "carbs": 18.0, "fat": 8.0, "category": "Indian Staples"},
    "Idli (2 pieces, 120g)":             {"cal": 130, "protein": 4.0, "carbs": 26.0, "fat": 0.8, "category": "Indian Staples"},
    "Dosa (1 plain, 100g)":              {"cal": 133, "protein": 3.4, "carbs": 20.0, "fat": 4.7, "category": "Indian Staples"},
    "Uttapam (1 medium, 120g)":          {"cal": 175, "protein": 5.0, "carbs": 25.0, "fat": 6.0, "category": "Indian Staples"},
    "Poha (1 cup, 150g)":                {"cal": 180, "protein": 4.0, "carbs": 32.0, "fat": 4.5, "category": "Indian Staples"},
    "Upma (1 cup, 160g)":                {"cal": 200, "protein": 4.5, "carbs": 30.0, "fat": 7.0, "category": "Indian Staples"},
    "Aloo Paratha (1 medium, 100g)":      {"cal": 310, "protein": 6.0, "carbs": 42.0, "fat": 13.0, "category": "Indian Staples"},
    "Paneer Paratha (1 medium, 100g)":    {"cal": 300, "protein": 12.0, "carbs": 35.0, "fat": 12.0, "category": "Indian Staples"},
    "Thepla (1 medium, 50g)":             {"cal": 140, "protein": 3.5, "carbs": 18.0, "fat": 6.0, "category": "Indian Staples"},

    # -- Rice & Grains --
    "White Rice (1 cup cooked, 186g)":  {"cal": 206, "protein": 4.3, "carbs": 44.5, "fat": 0.4, "category": "Rice & Grains"},
    "Brown Rice (1 cup cooked, 195g)":  {"cal": 216, "protein": 5.0, "carbs": 44.8, "fat": 1.8, "category": "Rice & Grains"},
    "Biryani (1 cup, 200g)":            {"cal": 310, "protein": 12.0, "carbs": 42.0, "fat": 10.0, "category": "Rice & Grains"},
    "Fried Rice (1 cup, 180g)":         {"cal": 240, "protein": 6.0, "carbs": 38.0, "fat": 8.0, "category": "Rice & Grains"},
    "Lemon Rice (1 cup, 180g)":         {"cal": 220, "protein": 4.5, "carbs": 38.0, "fat": 6.0, "category": "Rice & Grains"},
    "Jeera Rice (1 cup, 180g)":         {"cal": 210, "protein": 4.2, "carbs": 36.0, "fat": 5.5, "category": "Rice & Grains"},
    "Pulao (1 cup, 190g)":              {"cal": 240, "protein": 5.5, "carbs": 38.0, "fat": 7.0, "category": "Rice & Grains"},
    "Oats (1 cup cooked, 234g)":        {"cal": 166, "protein": 5.9, "carbs": 28.1, "fat": 3.6, "category": "Rice & Grains"},
    "Quinoa (1 cup cooked, 185g)":      {"cal": 222, "protein": 8.1, "carbs": 39.4, "fat": 3.6, "category": "Rice & Grains"},
    "Whole Wheat Bread (2 slices, 56g)": {"cal": 138, "protein": 7.0, "carbs": 23.0, "fat": 2.0, "category": "Rice & Grains"},
    "White Bread (2 slices, 56g)":       {"cal": 148, "protein": 4.8, "carbs": 26.0, "fat": 2.2, "category": "Rice & Grains"},
    "Muesli (1 cup, 85g)":              {"cal": 340, "protein": 9.0, "carbs": 60.0, "fat": 6.5, "category": "Rice & Grains"},
    "Cornflakes (1 cup, 30g)":          {"cal": 110, "protein": 2.0, "carbs": 24.0, "fat": 0.3, "category": "Rice & Grains"},

    # -- Dal & Legumes --
    "Moong Dal (1 cup cooked, 202g)":    {"cal": 210, "protein": 14.0, "carbs": 35.0, "fat": 0.8, "category": "Dal & Legumes"},
    "Masoor Dal (1 cup cooked, 198g)":   {"cal": 230, "protein": 18.0, "carbs": 39.0, "fat": 0.8, "category": "Dal & Legumes"},
    "Toor Dal (1 cup cooked, 200g)":     {"cal": 220, "protein": 13.0, "carbs": 37.0, "fat": 1.2, "category": "Dal & Legumes"},
    "Chana Dal (1 cup cooked, 210g)":    {"cal": 260, "protein": 15.0, "carbs": 41.0, "fat": 2.5, "category": "Dal & Legumes"},
    "Rajma / Kidney Beans (1 cup)":      {"cal": 225, "protein": 15.0, "carbs": 40.0, "fat": 0.8, "category": "Dal & Legumes"},
    "Kala Chana (1 cup)":                {"cal": 260, "protein": 15.0, "carbs": 44.0, "fat": 3.5, "category": "Dal & Legumes"},
    "Chole / Chickpeas (1 cup, 240g)":   {"cal": 269, "protein": 14.5, "carbs": 45.0, "fat": 4.2, "category": "Dal & Legumes"},
    "Lobia / Black Eyed Peas (1 cup)":   {"cal": 200, "protein": 13.0, "carbs": 35.0, "fat": 0.9, "category": "Dal & Legumes"},
    "Sprouts Moong (1 cup, 125g)":       {"cal": 100, "protein": 7.0, "carbs": 17.0, "fat": 0.4, "category": "Dal & Legumes"},
    "Soya Chunks (1 cup cooked, 100g)":  {"cal": 120, "protein": 24.0, "carbs": 8.0, "fat": 0.5, "category": "Dal & Legumes"},
    "Peanuts (1 oz, 28g)":              {"cal": 161, "protein": 7.3, "carbs": 4.6, "fat": 14.0, "category": "Dal & Legumes"},

    # -- Dairy --
    "Whole Milk (1 cup, 240ml)":        {"cal": 150, "protein": 8.0, "carbs": 12.0, "fat": 8.0, "category": "Dairy"},
    "Toned Milk (1 cup, 240ml)":        {"cal": 120, "protein": 8.0, "carbs": 12.0, "fat": 4.0, "category": "Dairy"},
    "Skimmed Milk (1 cup, 240ml)":      {"cal": 83,  "protein": 8.3, "carbs": 12.2, "fat": 0.2, "category": "Dairy"},
    "Curd / Yogurt (1 cup, 245g)":      {"cal": 149, "protein": 8.5, "carbs": 11.4, "fat": 8.0, "category": "Dairy"},
    "Low-fat Yogurt (1 cup, 245g)":     {"cal": 154, "protein": 12.9, "carbs": 17.2, "fat": 3.8, "category": "Dairy"},
    "Paneer (100g)":                     {"cal": 265, "protein": 18.3, "carbs": 3.6, "fat": 20.0, "category": "Dairy"},
    "Butter (1 tbsp, 14g)":             {"cal": 102, "protein": 0.1, "carbs": 0.0, "fat": 11.5, "category": "Dairy"},
    "Ghee (1 tbsp, 14g)":               {"cal": 120, "protein": 0.0, "carbs": 0.0, "fat": 13.8, "category": "Dairy"},
    "Cheese Cheddar (1 oz, 28g)":       {"cal": 113, "protein": 7.1, "carbs": 0.4, "fat": 9.3, "category": "Dairy"},
    "Cream Cheese (1 tbsp, 30g)":       {"cal": 50,  "protein": 0.9, "carbs": 0.8,  "fat": 4.9, "category": "Dairy"},
    "Lassi Sweet (1 glass, 300ml)":     {"cal": 220, "protein": 6.0, "carbs": 35.0, "fat": 6.0, "category": "Dairy"},
    "Buttermilk / Chaas (1 glass)":     {"cal": 60,  "protein": 3.0, "carbs": 7.0, "fat": 2.0, "category": "Dairy"},

    # -- Eggs & Non-Veg --
    "Egg (1 whole, boiled, 50g)":        {"cal": 78,  "protein": 6.3, "carbs": 0.6, "fat": 5.3, "category": "Eggs & Non-Veg"},
    "Egg White (1 large, 33g)":          {"cal": 17,  "protein": 3.6, "carbs": 0.2, "fat": 0.1, "category": "Eggs & Non-Veg"},
    "Egg Omelette (2 eggs)":             {"cal": 154, "protein": 12.0, "carbs": 1.0, "fat": 11.0, "category": "Eggs & Non-Veg"},
    "Chicken Breast (100g, cooked)":     {"cal": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6, "category": "Eggs & Non-Veg"},
    "Chicken Thigh (100g, cooked)":      {"cal": 209, "protein": 26.0, "carbs": 0.0, "fat": 10.9, "category": "Eggs & Non-Veg"},
    "Chicken Curry (1 cup, 240g)":       {"cal": 280, "protein": 25.0, "carbs": 6.0, "fat": 17.0, "category": "Eggs & Non-Veg"},
    "Butter Chicken (1 cup, 240g)":      {"cal": 400, "protein": 28.0, "carbs": 10.0, "fat": 28.0, "category": "Eggs & Non-Veg"},
    "Tandoori Chicken (1 piece, 150g)":  {"cal": 230, "protein": 30.0, "carbs": 2.0, "fat": 11.0, "category": "Eggs & Non-Veg"},
    "Fish / Rohu (100g, cooked)":        {"cal": 140, "protein": 20.0, "carbs": 0.0, "fat": 6.0, "category": "Eggs & Non-Veg"},
    "Prawns (100g, cooked)":             {"cal": 106, "protein": 20.0, "carbs": 0.0, "fat": 1.7, "category": "Eggs & Non-Veg"},
    "Mutton Curry (1 cup, 240g)":        {"cal": 320, "protein": 28.0, "carbs": 5.0, "fat": 21.0, "category": "Eggs & Non-Veg"},
    "Egg Biryani (1 cup, 200g)":         {"cal": 280, "protein": 11.0, "carbs": 38.0, "fat": 9.0, "category": "Eggs & Non-Veg"},
    "Keema (1 cup, 200g)":               {"cal": 280, "protein": 22.0, "carbs": 8.0, "fat": 18.0, "category": "Eggs & Non-Veg"},

    # -- Snacks --
    "Samosa (1 medium, 80g)":            {"cal": 250, "protein": 4.0, "carbs": 28.0, "fat": 14.0, "category": "Snacks"},
    "Pakora / Bhajia (100g)":            {"cal": 270, "protein": 5.0, "carbs": 25.0, "fat": 17.0, "category": "Snacks"},
    "Vada Pav (1 piece, 150g)":          {"cal": 330, "protein": 7.0, "carbs": 45.0, "fat": 14.0, "category": "Snacks"},
    "Burger (1 veg, 200g)":              {"cal": 350, "protein": 12.0, "carbs": 42.0, "fat": 15.0, "category": "Snacks"},
    "Pizza (1 slice, veg, 100g)":        {"cal": 260, "protein": 10.0, "carbs": 30.0, "fat": 11.0, "category": "Snacks"},
    "French Fries (1 medium, 117g)":     {"cal": 365, "protein": 4.0,  "carbs": 48.0, "fat": 17.0, "category": "Snacks"},
    "Maggi / Instant Noodles (1 pack)":  {"cal": 380, "protein": 8.0,  "carbs": 52.0, "fat": 14.0, "category": "Snacks"},
    "Pav Bhaji (1 plate)":               {"cal": 400, "protein": 8.0,  "carbs": 55.0, "fat": 16.0, "category": "Snacks"},
    "Chaat (1 plate)":                   {"cal": 280, "protein": 6.0,  "carbs": 40.0, "fat": 10.0, "category": "Snacks"},
    "Dhokla (1 piece, 50g)":             {"cal": 75,  "protein": 3.0,  "carbs": 12.0, "fat": 1.5, "category": "Snacks"},
    "Kachori (1 medium, 60g)":           {"cal": 210, "protein": 4.0,  "carbs": 24.0, "fat": 11.0, "category": "Snacks"},
    "Popcorn (1 cup, popped)":           {"cal": 31,  "protein": 1.0,  "carbs": 6.2,  "fat": 0.4, "category": "Snacks"},
    "Potato Chips (1 oz, 28g)":          {"cal": 152, "protein": 2.0,  "carbs": 15.0, "fat": 10.0, "category": "Snacks"},
    "Namkeen / Mixture (1 oz, 28g)":     {"cal": 140, "protein": 3.0,  "carbs": 12.0, "fat": 9.0, "category": "Snacks"},
    "Bhel Puri (1 cup, 100g)":           {"cal": 160, "protein": 3.0,  "carbs": 28.0, "fat": 4.5, "category": "Snacks"},
    "Sev Puri (1 plate, 6 pieces)":      {"cal": 220, "protein": 4.0,  "carbs": 30.0, "fat": 9.0, "category": "Snacks"},
    "Spring Roll (2 pieces)":            {"cal": 280, "protein": 5.0,  "carbs": 32.0, "fat": 14.0, "category": "Snacks"},

    # -- South Indian --
    "Masala Dosa (1 medium)":            {"cal": 210, "protein": 5.0,  "carbs": 30.0, "fat": 8.0, "category": "South Indian"},
    "Mysore Masala Dosa (1 medium)":     {"cal": 280, "protein": 6.0,  "carbs": 38.0, "fat": 12.0, "category": "South Indian"},
    "Rava Dosa (1 medium)":              {"cal": 185, "protein": 4.0,  "carbs": 26.0, "fat": 7.0, "category": "South Indian"},
    "Paper Dosa (1 large)":              {"cal": 140, "protein": 3.0,  "carbs": 22.0, "fat": 4.5, "category": "South Indian"},
    "Medu Vada (1 piece, 50g)":          {"cal": 95,  "protein": 3.0,  "carbs": 10.0, "fat": 4.5, "category": "South Indian"},
    "Sambar (1 cup, 240ml)":             {"cal": 150, "protein": 6.0,  "carbs": 20.0, "fat": 5.0, "category": "South Indian"},
    "Rasam (1 cup, 240ml)":              {"cal": 60,  "protein": 2.0,  "carbs": 8.0,  "fat": 2.0, "category": "South Indian"},
    "Coconut Chutney (2 tbsp, 30g)":     {"cal": 48,  "protein": 0.6,  "carbs": 1.8,  "fat": 4.5, "category": "South Indian"},
    "Curd Rice (1 cup, 200g)":           {"cal": 190, "protein": 6.0,  "carbs": 30.0, "fat": 5.0, "category": "South Indian"},
    "Pongal (1 cup, 200g)":              {"cal": 210, "protein": 6.0,  "carbs": 32.0, "fat": 7.0, "category": "South Indian"},

    # -- Curries & Main Dishes --
    "Dal Tadka (1 cup, 240g)":           {"cal": 180, "protein": 11.0, "carbs": 25.0, "fat": 4.5, "category": "Curries & Mains"},
    "Dal Fry (1 cup, 240g)":             {"cal": 200, "protein": 10.0, "carbs": 26.0, "fat": 6.0, "category": "Curries & Mains"},
    "Palak Paneer (1 cup, 240g)":        {"cal": 310, "protein": 15.0, "carbs": 10.0, "fat": 24.0, "category": "Curries & Mains"},
    "Paneer Butter Masala (1 cup)":      {"cal": 370, "protein": 16.0, "carbs": 14.0, "fat": 28.0, "category": "Curries & Mains"},
    "Paneer Tikka Masala (1 cup)":       {"cal": 340, "protein": 18.0, "carbs": 12.0, "fat": 25.0, "category": "Curries & Mains"},
    "Chole Masala (1 cup, 240g)":        {"cal": 280, "protein": 12.0, "carbs": 35.0, "fat": 10.0, "category": "Curries & Mains"},
    "Aloo Gobi (1 cup, 200g)":           {"cal": 180, "protein": 4.0,  "carbs": 25.0, "fat": 8.0, "category": "Curries & Mains"},
    "Baingan Bharta (1 cup, 200g)":      {"cal": 130, "protein": 3.5,  "carbs": 14.0, "fat": 7.0, "category": "Curries & Mains"},
    "Malai Kofta (1 cup, 240g)":         {"cal": 420, "protein": 10.0, "carbs": 30.0, "fat": 30.0, "category": "Curries & Mains"},
    "Rajma Masala (1 cup, 240g)":        {"cal": 240, "protein": 13.0, "carbs": 38.0, "fat": 4.0, "category": "Curries & Mains"},
    "Mixed Veg Curry (1 cup, 240g)":     {"cal": 170, "protein": 5.0,  "carbs": 20.0, "fat": 8.0, "category": "Curries & Mains"},
    "Kadhi Pakora (1 cup, 240g)":        {"cal": 220, "protein": 8.0,  "carbs": 22.0, "fat": 11.0, "category": "Curries & Mains"},
    "Butter Naan (1 piece, 90g)":        {"cal": 310, "protein": 8.0,  "carbs": 48.0, "fat": 10.0, "category": "Curries & Mains"},
    "Garlic Naan (1 piece, 90g)":        {"cal": 320, "protein": 8.5,  "carbs": 46.0, "fat": 11.0, "category": "Curries & Mains"},

    # -- Beverages --
    "Tea / Chai (1 cup, 200ml)":         {"cal": 38,  "protein": 0.5, "carbs": 7.0,  "fat": 0.8, "category": "Beverages"},
    "Coffee Black (1 cup, 200ml)":       {"cal": 5,   "protein": 0.3, "carbs": 0.0,  "fat": 0.0, "category": "Beverages"},
    "Coffee with Milk (1 cup, 200ml)":   {"cal": 60,  "protein": 2.0, "carbs": 8.0,  "fat": 2.5, "category": "Beverages"},
    "Green Tea (1 cup, 200ml)":          {"cal": 2,   "protein": 0.5, "carbs": 0.0,  "fat": 0.0, "category": "Beverages"},
    "Fresh Lime Water (1 glass)":        {"cal": 40,  "protein": 0.2, "carbs": 10.0, "fat": 0.1, "category": "Beverages"},
    "Orange Juice (1 glass, 240ml)":     {"cal": 112, "protein": 1.7, "carbs": 25.8, "fat": 0.5, "category": "Beverages"},
    "Mango Shake (1 glass, 300ml)":      {"cal": 250, "protein": 5.0, "carbs": 42.0, "fat": 7.0, "category": "Beverages"},
    "Banana Shake (1 glass, 300ml)":     {"cal": 230, "protein": 6.0, "carbs": 40.0, "fat": 5.0, "category": "Beverages"},
    "Protein Shake (1 scoop + water)":   {"cal": 120, "protein": 24.0, "carbs": 3.0, "fat": 1.5, "category": "Beverages"},
    "Coca-Cola (1 can, 330ml)":          {"cal": 139, "protein": 0.0, "carbs": 35.0, "fat": 0.0, "category": "Beverages"},
    "Packaged Juice (1 tetra, 200ml)":   {"cal": 110, "protein": 0.5, "carbs": 26.0, "fat": 0.2, "category": "Beverages"},
    "Coconut Water (1 glass, 330ml)":    {"cal": 60,  "protein": 0.7, "carbs": 15.0, "fat": 0.2, "category": "Beverages"},

    # -- Sweets & Desserts --
    "Gulab Jamun (2 pieces, 100g)":      {"cal": 310, "protein": 4.0,  "carbs": 50.0, "fat": 12.0, "category": "Sweets & Desserts"},
    "Rasgulla (2 pieces, 100g)":         {"cal": 186, "protein": 4.0,  "carbs": 38.0, "fat": 2.0, "category": "Sweets & Desserts"},
    "Jalebi (2 pieces, 60g)":            {"cal": 200, "protein": 2.0,  "carbs": 35.0, "fat": 6.0, "category": "Sweets & Desserts"},
    "Kheer (1 cup, 200g)":               {"cal": 220, "protein": 6.0,  "carbs": 30.0, "fat": 9.0, "category": "Sweets & Desserts"},
    "Halwa (1 cup, 200g)":               {"cal": 320, "protein": 5.0,  "carbs": 45.0, "fat": 14.0, "category": "Sweets & Desserts"},
    "Barfi (2 pieces, 50g)":             {"cal": 180, "protein": 3.0,  "carbs": 25.0, "fat": 8.0, "category": "Sweets & Desserts"},
    "Ladoo (1 medium, 40g)":             {"cal": 150, "protein": 2.5,  "carbs": 20.0, "fat": 7.0, "category": "Sweets & Desserts"},
    "Ice Cream (1 scoop, 70g)":          {"cal": 140, "protein": 2.5,  "carbs": 18.0, "fat": 7.0, "category": "Sweets & Desserts"},
    "Chocolate (1 bar, 40g)":            {"cal": 210, "protein": 2.5,  "carbs": 24.0, "fat": 13.0, "category": "Sweets & Desserts"},
    "Cake (1 slice, 80g)":               {"cal": 300, "protein": 3.5,  "carbs": 40.0, "fat": 14.0, "category": "Sweets & Desserts"},
    "Modak (1 piece, 30g)":              {"cal": 100, "protein": 1.5,  "carbs": 16.0, "fat": 3.5, "category": "Sweets & Desserts"},
    "Kulfi (1 piece, 70g)":              {"cal": 160, "protein": 4.0,  "carbs": 20.0, "fat": 8.0, "category": "Sweets & Desserts"},

    # -- Nuts & Seeds --
    "Almonds (1 oz, ~23 nuts)":          {"cal": 164, "protein": 6.0, "carbs": 6.1, "fat": 14.2, "category": "Nuts & Seeds"},
    "Cashews (1 oz, ~18 nuts)":          {"cal": 157, "protein": 5.2, "carbs": 8.6, "fat": 12.4, "category": "Nuts & Seeds"},
    "Walnuts (1 oz, ~14 halves)":        {"cal": 185, "protein": 4.3, "carbs": 3.9, "fat": 18.5, "category": "Nuts & Seeds"},
    "Pistachios (1 oz, ~49 nuts)":       {"cal": 159, "protein": 5.7, "carbs": 7.7, "fat": 12.9, "category": "Nuts & Seeds"},
    "Raisins (1 oz, 28g)":               {"cal": 85,  "protein": 0.9, "carbs": 22.0, "fat": 0.1, "category": "Nuts & Seeds"},
    "Dates (1 date, 24g)":               {"cal": 66,  "protein": 0.4, "carbs": 18.0, "fat": 0.0, "category": "Nuts & Seeds"},
    "Flax Seeds (1 tbsp, 10g)":          {"cal": 55,  "protein": 1.9, "carbs": 3.0, "fat": 4.3, "category": "Nuts & Seeds"},
    "Chia Seeds (1 tbsp, 12g)":          {"cal": 58,  "protein": 2.0, "carbs": 5.1, "fat": 3.7, "category": "Nuts & Seeds"},
    "Sunflower Seeds (1 oz, 28g)":       {"cal": 165, "protein": 5.5, "carbs": 6.5, "fat": 14.0, "category": "Nuts & Seeds"},
    "Makhana / Fox Nuts (1 oz, 28g)":    {"cal": 103, "protein": 3.6, "carbs": 7.7, "fat": 0.3, "category": "Nuts & Seeds"},

    # -- Oils & Fats --
    "Olive Oil (1 tbsp, 14ml)":          {"cal": 119, "protein": 0.0, "carbs": 0.0, "fat": 13.5, "category": "Oils & Fats"},
    "Mustard Oil (1 tbsp, 14ml)":        {"cal": 120, "protein": 0.0, "carbs": 0.0, "fat": 13.6, "category": "Oils & Fats"},
    "Coconut Oil (1 tbsp, 14ml)":        {"cal": 121, "protein": 0.0, "carbs": 0.0, "fat": 13.5, "category": "Oils & Fats"},

    # -- Condiments --
    "Honey (1 tbsp, 21g)":               {"cal": 64,  "protein": 0.1, "carbs": 17.3, "fat": 0.0, "category": "Condiments"},
    "Sugar (1 tsp, 4g)":                 {"cal": 16,  "protein": 0.0, "carbs": 4.0,  "fat": 0.0, "category": "Condiments"},
    "Jam (1 tbsp, 20g)":                 {"cal": 52,  "protein": 0.1, "carbs": 13.0, "fat": 0.0, "category": "Condiments"},
    "Ketchup (1 tbsp, 17g)":             {"cal": 20,  "protein": 0.1, "carbs": 5.0,  "fat": 0.0, "category": "Condiments"},
    "Mayonnaise (1 tbsp, 15g)":          {"cal": 94,  "protein": 0.1, "carbs": 0.1,  "fat": 10.3, "category": "Condiments"},
    "Peanut Butter (2 tbsp, 32g)":       {"cal": 188, "protein": 8.0, "carbs": 6.0,  "fat": 16.0, "category": "Condiments"},

    # -- Fast Food & International --
    "Momos Veg (4 pieces)":              {"cal": 200, "protein": 5.0, "carbs": 30.0, "fat": 7.0, "category": "Fast Food"},
    "Momos Chicken (4 pieces)":          {"cal": 220, "protein": 10.0, "carbs": 28.0, "fat": 8.0, "category": "Fast Food"},
    "Thukpa (1 bowl, 350ml)":            {"cal": 250, "protein": 8.0, "carbs": 35.0, "fat": 8.0, "category": "Fast Food"},
    "Frankie / Wrap (1 roll)":           {"cal": 300, "protein": 10.0, "carbs": 38.0, "fat": 12.0, "category": "Fast Food"},
    "Pasta (1 cup, 200g)":               {"cal": 280, "protein": 10.0, "carbs": 42.0, "fat": 8.0, "category": "Fast Food"},
    "Sandwich (1 veg, 150g)":            {"cal": 260, "protein": 9.0, "carbs": 34.0, "fat": 10.0, "category": "Fast Food"},
    "Chowmein (1 cup, 200g)":            {"cal": 260, "protein": 7.0, "carbs": 38.0, "fat": 9.0, "category": "Fast Food"},
    "Manchurian (1 cup, 200g)":          {"cal": 220, "protein": 5.0, "carbs": 25.0, "fat": 11.0, "category": "Fast Food"},
    "Hakka Noodles (1 cup, 200g)":       {"cal": 280, "protein": 7.0, "carbs": 42.0, "fat": 9.0, "category": "Fast Food"},
    "Tacos (1 piece, veg)":              {"cal": 220, "protein": 8.0, "carbs": 26.0, "fat": 9.0, "category": "Fast Food"},
}

# ================= MEAL TYPES =================
MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]

# ================= HELPER FUNCTIONS =================

def get_categories():
    categories = set()
    for item in food_database.values():
        categories.add(item["category"])
    return sorted(categories)


def get_todays_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_todays_time():
    return datetime.now().strftime("%H:%M:%S")


# ================= REGISTER =================

def register_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Fill all fields")
        return

    if len(password) < 4:
        messagebox.showerror("Error", "Password must be at least 4 characters")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, password)
        )
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful! You can now log in.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

    conn.close()


# ================= LOGIN =================

def login_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Fill all fields")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid username or password")


# ================= DASHBOARD =================

def open_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title(f"NutriTrack - {username}")
    dashboard.geometry("950x720")
    dashboard.configure(bg="#f0f2f5")
    dashboard.resizable(True, True)

    total_cal_var = tk.StringVar(value="0")
    goal_cal_var = tk.StringVar(value="--")
    remaining_cal_var = tk.StringVar(value="--")
    protein_var = tk.StringVar(value="0g")
    carbs_var = tk.StringVar(value="0g")
    fat_var = tk.StringVar(value="0g")
    water_var = tk.StringVar(value="0 / 8")
    status_var = tk.StringVar(value="")
    progress_var = tk.DoubleVar(value=0)
    water_display_text = tk.StringVar(value="Glasses: 0")

    # ── Header ──
    header_frame = tk.Frame(dashboard, bg="#2c3e50", height=60)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame, text=f"NutriTrack - {username}",
        font=("Segoe UI", 16, "bold"), fg="white", bg="#2c3e50"
    ).pack(side="left", padx=15, pady=12)

    tk.Label(
        header_frame, text=f"Date: {get_todays_date()}",
        font=("Segoe UI", 11), fg="#bdc3c7", bg="#2c3e50"
    ).pack(side="right", padx=15)

    # ── Main container ──
    main_frame = tk.Frame(dashboard, bg="#f0f2f5")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ── LEFT PANEL ──
    left_panel = tk.Frame(main_frame, bg="white", bd=1, relief="groove", width=310)
    left_panel.pack(side="left", fill="y", padx=(0, 5))
    left_panel.pack_propagate(False)

    tk.Label(
        left_panel, text="Add Food Entry",
        font=("Segoe UI", 13, "bold"), bg="white", fg="#2c3e50"
    ).pack(pady=(10, 5), padx=10)

    # Category filter
    tk.Label(left_panel, text="Category:", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=10)
    category_var = tk.StringVar(value="All Categories")
    category_names = ["All Categories"] + get_categories()
    category_menu = ttk.Combobox(
        left_panel, textvariable=category_var,
        values=category_names, state="readonly", width=32
    )
    category_menu.pack(padx=10, pady=2)

    # Food selection
    tk.Label(left_panel, text="Food Item:", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=10)
    food_var = tk.StringVar()
    food_menu = ttk.Combobox(
        left_panel, textvariable=food_var,
        values=list(food_database.keys()), state="readonly", width=38
    )
    food_menu.pack(padx=10, pady=2)
    if list(food_database.keys()):
        food_var.set(list(food_database.keys())[0])

    def update_food_list(*args):
        cat = category_var.get()
        if cat == "All Categories":
            filtered = list(food_database.keys())
        else:
            filtered = [k for k, v in food_database.items() if v["category"] == cat]
        food_menu["values"] = filtered
        if filtered:
            food_var.set(filtered[0])

    category_menu.bind("<<ComboboxSelected>>", update_food_list)

    # Quantity
    tk.Label(left_panel, text="Quantity (servings):", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=10)
    qty_entry = tk.Entry(left_panel, width=10, font=("Segoe UI", 10))
    qty_entry.insert(0, "1")
    qty_entry.pack(padx=10, pady=2)

    # Meal type
    tk.Label(left_panel, text="Meal Type:", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=10)
    meal_var = tk.StringVar(value="Breakfast")
    meal_menu = ttk.Combobox(
        left_panel, textvariable=meal_var,
        values=MEAL_TYPES, state="readonly", width=20
    )
    meal_menu.pack(padx=10, pady=2)

    # Preview
    preview_frame = tk.LabelFrame(left_panel, text="Per Serving Nutrition", font=("Segoe UI", 9), bg="white", fg="#7f8c8d")
    preview_frame.pack(padx=10, pady=5, fill="x")

    preview_cal = tk.Label(preview_frame, text="Cal: --", font=("Segoe UI", 9), bg="white")
    preview_cal.pack(anchor="w", padx=5)
    preview_macros = tk.Label(preview_frame, text="P: -- | C: -- | F: --", font=("Segoe UI", 9), bg="white")
    preview_macros.pack(anchor="w", padx=5)

    def update_preview(*args):
        sel = food_var.get()
        if sel in food_database:
            info = food_database[sel]
            preview_cal.config(text=f"Cal: {info['cal']} kcal")
            preview_macros.config(
                text=f"P: {info['protein']}g | C: {info['carbs']}g | F: {info['fat']}g"
            )

    food_menu.bind("<<ComboboxSelected>>", update_preview)
    if food_var.get():
        update_preview()

    def add_food_entry(user):
        try:
            food = food_var.get()
            qty = int(qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive quantity")
            return

        if food not in food_database:
            messagebox.showerror("Error", "Select a food item")
            return

        info = food_database[food]
        total_cal = info["cal"] * qty
        total_protein = info["protein"] * qty
        total_carbs = info["carbs"] * qty
        total_fat = info["fat"] * qty
        meal = meal_var.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO food_log
               (username, food_name, calories, protein, carbs, fat, serving_size, meal_type, log_date, log_time)
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user, food, total_cal, total_protein, total_carbs, total_fat, f"{qty} serving(s)", meal, get_todays_date(), get_todays_time())
        )
        conn.commit()
        conn.close()

        qty_entry.delete(0, tk.END)
        qty_entry.insert(0, "1")
        refresh_all()

    # Add button
    tk.Button(
        left_panel, text="Add Food", font=("Segoe UI", 11, "bold"),
        bg="#27ae60", fg="white", width=22,
        command=lambda: add_food_entry(username)
    ).pack(pady=8, padx=10)

    # Search box
    tk.Label(left_panel, text="Search Food:", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=10, pady=(10, 0))
    search_entry = tk.Entry(left_panel, width=32, font=("Segoe UI", 10))
    search_entry.pack(padx=10, pady=2)

    def search_food(*args):
        query = search_entry.get().strip().lower()
        if not query:
            update_food_list()
        else:
            filtered = [k for k in food_database.keys() if query in k.lower()]
            food_menu["values"] = filtered
            if filtered:
                food_var.set(filtered[0])

    search_entry.bind("<KeyRelease>", search_food)

    # Water tracking
    water_frame = tk.LabelFrame(left_panel, text="Water Intake", font=("Segoe UI", 10), bg="white", fg="#2980b9")
    water_frame.pack(padx=10, pady=8, fill="x")

    water_label = tk.Label(water_frame, textvariable=water_display_text, font=("Segoe UI", 11, "bold"), bg="white", fg="#2980b9")
    water_label.pack()

    water_btn_frame = tk.Frame(water_frame, bg="white")
    water_btn_frame.pack()

    def add_water():
        conn = get_connection()
        cursor = conn.cursor()
        today = get_todays_date()
        cursor.execute("SELECT glasses FROM water_log WHERE username=? AND log_date=?", (username, today))
        row = cursor.fetchone()
        if row:
            cursor.execute("UPDATE water_log SET glasses=glasses+1 WHERE username=? AND log_date=?", (username, today))
        else:
            cursor.execute("INSERT INTO water_log(username, glasses, log_date) VALUES(?, 1, ?)", (username, today))
        conn.commit()
        conn.close()
        refresh_all()

    def remove_water():
        conn = get_connection()
        cursor = conn.cursor()
        today = get_todays_date()
        cursor.execute("SELECT glasses FROM water_log WHERE username=? AND log_date=?", (username, today))
        row = cursor.fetchone()
        if row and row[0] > 0:
            cursor.execute("UPDATE water_log SET glasses=glasses-1 WHERE username=? AND log_date=?", (username, today))
            conn.commit()
        conn.close()
        refresh_all()

    tk.Button(water_btn_frame, text=" + ", font=("Segoe UI", 10), bg="#3498db", fg="white",
              command=add_water).pack(side="left", padx=3)
    tk.Button(water_btn_frame, text=" - ", font=("Segoe UI", 10), bg="#e74c3c", fg="white",
              command=remove_water).pack(side="left", padx=3)

    # Set Goals button
    def open_goals():
        goal_window = tk.Toplevel(dashboard)
        goal_window.title("Set Goals")
        goal_window.geometry("350x400")
        goal_window.configure(bg="white")

        tk.Label(goal_window, text="Set Your Daily Goals", font=("Segoe UI", 13, "bold"), bg="white").pack(pady=10)

        fields = {}
        for label, key in [("Calorie Goal (kcal)", "calorie_goal"), ("Protein Goal (g)", "protein_goal"),
                           ("Carbs Goal (g)", "carb_goal"), ("Fat Goal (g)", "fat_goal"),
                           ("Water Goal (glasses)", "water_goal")]:
            tk.Label(goal_window, text=label, font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=20)
            entry = tk.Entry(goal_window, width=20, font=("Segoe UI", 10))
            entry.pack(padx=20, pady=2)
            fields[key] = entry

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT calorie_goal, protein_goal, carb_goal, fat_goal, water_goal FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            for i, key in enumerate(fields):
                fields[key].insert(0, str(row[i]))

        def save_goals():
            try:
                vals = [int(fields[k].get()) for k in fields]
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers")
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET calorie_goal=?, protein_goal=?, carb_goal=?, fat_goal=?, water_goal=? WHERE username=?",
                (*vals, username)
            )
            conn.commit()
            conn.close()
            goal_window.destroy()
            refresh_all()

        tk.Button(goal_window, text="Save Goals", font=("Segoe UI", 11, "bold"), bg="#2c3e50", fg="white",
                  command=save_goals).pack(pady=15)

    tk.Button(
        left_panel, text="Set Goals", font=("Segoe UI", 10),
        bg="#2980b9", fg="white", width=22,
        command=open_goals
    ).pack(pady=2, padx=10)

    # ── CENTER PANEL ──
    center_panel = tk.Frame(main_frame, bg="#f0f2f5")
    center_panel.pack(side="left", fill="both", expand=True, padx=5)

    # Summary card
    summary_card = tk.Frame(center_panel, bg="white", bd=1, relief="groove")
    summary_card.pack(fill="x", pady=(0, 5))

    tk.Label(
        summary_card, text="Today's Summary",
        font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50"
    ).pack(pady=(8, 3))

    # Progress bar
    progress_frame = tk.Frame(summary_card, bg="white")
    progress_frame.pack(fill="x", padx=15, pady=3)
    progress_bar = ttk.Progressbar(
        progress_frame, variable=progress_var,
        maximum=100, length=550, mode="determinate"
    )
    progress_bar.pack(fill="x")

    # Calorie labels
    cal_frame = tk.Frame(summary_card, bg="white")
    cal_frame.pack(fill="x", padx=15, pady=5)

    tk.Label(cal_frame, text="Consumed:", font=("Segoe UI", 10), bg="white").pack(side="left")
    tk.Label(cal_frame, textvariable=total_cal_var, font=("Segoe UI", 11, "bold"), bg="white", fg="#e74c3c").pack(side="left", padx=5)

    tk.Label(cal_frame, text="Goal:", font=("Segoe UI", 10), bg="white").pack(side="left", padx=(15, 0))
    tk.Label(cal_frame, textvariable=goal_cal_var, font=("Segoe UI", 11, "bold"), bg="white", fg="#2c3e50").pack(side="left", padx=5)

    tk.Label(cal_frame, text="Remaining:", font=("Segoe UI", 10), bg="white").pack(side="left", padx=(15, 0))
    tk.Label(cal_frame, textvariable=remaining_cal_var, font=("Segoe UI", 11, "bold"), bg="white", fg="#27ae60").pack(side="left", padx=5)

    # Macros
    macros_frame = tk.Frame(summary_card, bg="white")
    macros_frame.pack(fill="x", padx=15, pady=(0, 10))

    tk.Label(macros_frame, text="Protein:", font=("Segoe UI", 10), bg="white").pack(side="left")
    tk.Label(macros_frame, textvariable=protein_var, font=("Segoe UI", 10, "bold"), bg="white").pack(side="left", padx=(2, 15))

    tk.Label(macros_frame, text="Carbs:", font=("Segoe UI", 10), bg="white").pack(side="left")
    tk.Label(macros_frame, textvariable=carbs_var, font=("Segoe UI", 10, "bold"), bg="white").pack(side="left", padx=(2, 15))

    tk.Label(macros_frame, text="Fat:", font=("Segoe UI", 10), bg="white").pack(side="left")
    tk.Label(macros_frame, textvariable=fat_var, font=("Segoe UI", 10, "bold"), bg="white").pack(side="left", padx=(2, 15))

    tk.Label(macros_frame, text="Water:", font=("Segoe UI", 10), bg="white").pack(side="left")
    tk.Label(macros_frame, textvariable=water_var, font=("Segoe UI", 10, "bold"), bg="white", fg="#2980b9").pack(side="left", padx=2)

    tk.Label(summary_card, textvariable=status_var, font=("Segoe UI", 10, "italic"), bg="white", fg="#e67e22").pack(pady=(0, 8))

    # ── Meal-wise food log with tabs ──
    log_notebook = ttk.Notebook(center_panel)
    log_notebook.pack(fill="both", expand=True)

    tree_refs = {}

    for meal in MEAL_TYPES:
        frame = tk.Frame(log_notebook, bg="white")
        log_notebook.add(frame, text=f"  {meal}  ")

        tree = ttk.Treeview(frame, columns=("food", "qty", "cal", "protein", "carbs", "fat", "time", "id"),
                            show="headings", height=8)
        tree.heading("food", text="Food")
        tree.heading("qty", text="Qty")
        tree.heading("cal", text="Calories")
        tree.heading("protein", text="Protein(g)")
        tree.heading("carbs", text="Carbs(g)")
        tree.heading("fat", text="Fat(g)")
        tree.heading("time", text="Time")
        tree.heading("id", text="ID")

        tree.column("food", width=220)
        tree.column("qty", width=60)
        tree.column("cal", width=70)
        tree.column("protein", width=75)
        tree.column("carbs", width=70)
        tree.column("fat", width=55)
        tree.column("time", width=65)
        tree.column("id", width=0, stretch=False)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tree_refs[meal] = tree

    # Delete selected button
    btn_frame = tk.Frame(center_panel, bg="#f0f2f5")
    btn_frame.pack(fill="x", pady=3)

    def delete_selected():
        current_tab = log_notebook.index(log_notebook.select())
        current_meal = MEAL_TYPES[current_tab]
        tree = tree_refs[current_meal]
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to delete")
            return

        entry_id = tree.item(selected[0])["values"][-1]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_log WHERE id=?", (entry_id,))
        conn.commit()
        conn.close()
        refresh_all()

    def delete_all_today():
        confirm = messagebox.askyesno("Confirm", "Delete ALL entries for today?")
        if not confirm:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_log WHERE username=? AND log_date=?", (username, get_todays_date()))
        cursor.execute("DELETE FROM water_log WHERE username=? AND log_date=?", (username, get_todays_date()))
        conn.commit()
        conn.close()
        refresh_all()

    tk.Button(btn_frame, text="Delete Selected", font=("Segoe UI", 9), bg="#e74c3c", fg="white",
              command=delete_selected).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear All Today", font=("Segoe UI", 9), bg="#c0392b", fg="white",
              command=delete_all_today).pack(side="left", padx=5)

    # ── Refresh function ──
    def refresh_all():
        conn = get_connection()
        cursor = conn.cursor()

        # Get goals
        cursor.execute(
            "SELECT calorie_goal, protein_goal, carb_goal, fat_goal, water_goal FROM users WHERE username=?",
            (username,)
        )
        goals = cursor.fetchone()
        goal_cal = goals[0] if goals else 2000
        goal_protein = goals[1] if goals else 150
        goal_carbs = goals[2] if goals else 250
        goal_fat = goals[3] if goals else 65
        goal_water = goals[4] if goals else 8

        goal_cal_var.set(f"{goal_cal} kcal")

        today = get_todays_date()

        # Get today's food log
        cursor.execute(
            "SELECT id, food_name, calories, protein, carbs, fat, serving_size, meal_type, log_time FROM food_log WHERE username=? AND log_date=?",
            (username, today)
        )
        rows = cursor.fetchall()

        # Clear all trees
        for meal in MEAL_TYPES:
            tree_refs[meal].delete(*tree_refs[meal].get_children())

        total_cal = 0
        total_protein = 0.0
        total_carbs = 0.0
        total_fat = 0.0

        for row in rows:
            entry_id, food_name, calories, protein, carbs, fat, serving, meal, log_time = row
            total_cal += calories
            total_protein += protein
            total_carbs += carbs
            total_fat += fat

            meal_key = meal if meal in tree_refs else "Other"
            tree_refs[meal_key].insert("", "end", values=(
                food_name, serving, calories,
                f"{protein:.1f}", f"{carbs:.1f}", f"{fat:.1f}",
                log_time, entry_id
            ))

        # Get water
        cursor.execute("SELECT glasses FROM water_log WHERE username=? AND log_date=?", (username, today))
        water_row = cursor.fetchone()
        water_glasses = water_row[0] if water_row else 0

        conn.close()

        total_cal_var.set(f"{total_cal} kcal")
        remaining = goal_cal - total_cal
        if remaining >= 0:
            remaining_cal_var.set(f"{remaining} kcal")
            status_var.set("")
        else:
            remaining_cal_var.set(f"{abs(remaining)} kcal OVER")
            status_var.set("You have exceeded your calorie goal!")

        protein_var.set(f"{total_protein:.1f}g / {goal_protein}g")
        carbs_var.set(f"{total_carbs:.1f}g / {goal_carbs}g")
        fat_var.set(f"{total_fat:.1f}g / {goal_fat}g")
        water_var.set(f"{water_glasses} / {goal_water}")
        water_display_text.set(f"Glasses: {water_glasses}")

        if goal_cal > 0:
            pct = min((total_cal / goal_cal) * 100, 100)
            progress_var.set(pct)
        else:
            progress_var.set(0)

    refresh_all()


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("NutriTrack - Calorie Counter")
root.geometry("420x380")
root.configure(bg="#ecf0f1")
root.resizable(False, False)

# Main frame
main = tk.Frame(root, bg="#ecf0f1")
main.pack(expand=True)

tk.Label(
    main, text="NutriTrack",
    font=("Segoe UI", 24, "bold"), bg="#ecf0f1", fg="#2c3e50"
).pack(pady=(20, 5))

tk.Label(
    main, text="Track your calories, macros & water intake",
    font=("Segoe UI", 10), bg="#ecf0f1", fg="#7f8c8d"
).pack(pady=(0, 20))

# Login frame
login_frame = tk.Frame(main, bg="white", bd=1, relief="groove")
login_frame.pack(padx=20, pady=5, fill="x")

tk.Label(login_frame, text="Username", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=20, pady=(10, 0))
username_entry = tk.Entry(login_frame, width=35, font=("Segoe UI", 10))
username_entry.pack(padx=20, pady=2)

tk.Label(login_frame, text="Password", font=("Segoe UI", 10), bg="white").pack(anchor="w", padx=20)
password_entry = tk.Entry(login_frame, width=35, font=("Segoe UI", 10), show="*")
password_entry.pack(padx=20, pady=(2, 10))

# Buttons
btn_frame = tk.Frame(main, bg="#ecf0f1")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame, text="Register", font=("Segoe UI", 11),
    bg="#3498db", fg="white", width=12,
    command=register_user
).pack(side="left", padx=5)

tk.Button(
    btn_frame, text="Login", font=("Segoe UI", 11),
    bg="#27ae60", fg="white", width=12,
    command=login_user
).pack(side="left", padx=5)

# Bind Enter key
password_entry.bind("<Return>", lambda e: login_user())

# Footer
tk.Label(
    root, text="Food database: 170+ items | Track calories, protein, carbs, fat & water",
    font=("Segoe UI", 8), bg="#ecf0f1", fg="#95a5a6"
).pack(side="bottom", pady=5)

root.mainloop()