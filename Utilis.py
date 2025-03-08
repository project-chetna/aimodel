import os
import psycopg2
import numpy as np
import face_recognition
from PIL import Image
from psycopg2.extras import RealDictCursor
from flask import jsonify

# Database connection parametersaa
DB_HOST = 'face-opop.g.aivencloud.com'
DB_PORT = '21703'
DB_USER = 'avnadmin'
DB_PASSWORD = 'AVNS_X20xXPQrX-lExpXvOyo'
DB_NAME = 'defaultdb'

# Directory to save images
IMAGE_DIR = 'images'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


def connect_db():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )


def store_image(file):
    """Stores an image, extracts its face encoding, and saves it in the database."""
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Read image and convert to numpy array
         

        img = Image.open(file.stream)
         
         
         
        img=np.array(img)
         

        # Save the image
        image_path = os.path.join(IMAGE_DIR, file.filename)
         
        Image.fromarray(img).save(image_path)
        print(img)
        print(f"🟢 Detecting.......")
        
        # Extract face encoding
        encodings = face_recognition.face_encodings(img)
        print("after")
        if len(encodings) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400
         
        encoding_binary = np.array(encodings[0], dtype=np.float32).tobytes()
         
        # Insert into database
        cur.execute("INSERT INTO faces (filename, embedding) VALUES (%s, %s) RETURNING id",
                    (file.filename, psycopg2.Binary(encoding_binary)))
        conn.commit()
        image_id = cur.fetchone()[0]
        cur.close()
        conn.close()

        return jsonify({'message': 'Image stored successfully', 'image_id': image_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def verify_image(file):
    """Verifies an uploaded image against stored face encodings using cosine similarity."""
    try:
        conn = connect_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Read and preprocess image
        img = Image.open(file.stream)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = np.array(img)

        # Extract face encoding
        query_encodings = face_recognition.face_encodings(img)
        if len(query_encodings) == 0:
            return jsonify({'error': 'No face detected in the image'}), 400

        query_embedding = query_encodings[0]

        # Fetch stored embeddings
        cur.execute("SELECT id, filename, embedding FROM faces")
        rows = cur.fetchall()

        if not rows:
            return jsonify({'message': 'No faces stored in the database'}), 404

        # Convert all stored embeddings to a NumPy array for batch processing
        embeddings = []
        filenames = []
        for row in rows:
            db_embedding = np.frombuffer(row['embedding'], dtype=np.float32)
            if len(query_embedding) == len(db_embedding):  # Ensure same dimensions
                embeddings.append(db_embedding)
                filenames.append(row['filename'])

        if not embeddings:
            return jsonify({'message': 'No valid embeddings found in the database'}), 404

        embeddings = np.array(embeddings)

        # Compute cosine similarity
        query_norm = np.linalg.norm(query_embedding)
        db_norms = np.linalg.norm(embeddings, axis=1)
        similarities = np.dot(embeddings, query_embedding) / (db_norms * query_norm)

        # Find best match
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]
        matched_image = filenames[best_idx]

        cur.close()
        conn.close()

        # Set a similarity threshold for a valid match (adjustable)
        SIMILARITY_THRESHOLD = 0.65  # Can be tuned based on testing

        if best_similarity >= SIMILARITY_THRESHOLD:
            return jsonify({
                'message': 'Match found',
                'matched_image': matched_image,
                'similarity': float(best_similarity)
            }), 200
        else:
            return jsonify({'message': 'No match found', 'similarity': float(best_similarity)}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    except Exception as e:
        return jsonify({'error': str(e)}), 500
