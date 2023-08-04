import random
import json

import streamlit as st

from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue

from qdrant_connection import QDrantConnection

# qdrant connector demo code
def main():
  config = json.load(open('config.json'))

  conn = st.experimental_connection('qdrant', type=QDrantConnection,
    url=config['url'], api_key=config['api_key']
  )
  print(conn)

  cursor = conn.cursor()
  print(cursor)

  # collection vars
  collection_name = 'myTestCollection'
  vector_size = 5

  # delete collection
  conn.delete_collection(collection_name)

  # create a collection
  conn.create_collection(collection_name,
    VectorParams(size=vector_size, distance=Distance.COSINE))
  
  # add vectors to collection
  points = qdrant_addVectors(conn, collection_name, vector_size)

  # get collection
  collection = conn.get_collection(collection_name)
  print('-----\ncollection:')
  print(collection)

  # query with filtering
  qdrant_filter(conn, collection_name, points[0].vector, vector_size)

# demo code for adding vectors
def qdrant_addVectors(conn, collection_name, vector_size):
  # generate random list of vectors
  cities = [
    'London',
    'Berlin',
    'Paris',
    'Madrid',
    'Amsterdam',
    'Brussels',
    'Warsaw',
    'Zurich',
    'Vienna',
    'Rome',
    'Prague',
    'Lisbon'
  ]

  points = []

  for i in range(25):
    # build vector
    vector = []

    for _ in range(vector_size):
      vector.append(random.random())

    # build payload
    containsAllCountries = False
    stop = False

    payload = {'city': []}

    while(not containsAllCountries and not stop):
      # choose random city to add
      city = random.choice(cities)

      if(not city in payload['city']):
        payload['city'].append(city)

      containsAllCountries = len(payload['city']) == len(cities)

      # randomly choose to stop so all cities are not always chosen
      stop = random.random() < 0.3

    # add point
    points.append(PointStruct(id=i, vector=vector, payload=payload))

  print('-----\npoints:')
  print(points)

  conn.add_vectors(collection_name, points)

  return points

# demo of filter capability
def qdrant_filter(conn, collection_name, vector, vector_size):
  # build filter
  filter = Filter(
    must=[
      FieldCondition(
        key='city',
        match=MatchValue(value='London')
      )
    ]
  )

  print('-----\nfilter:')
  print(filter)

  filteredCollection = conn.query(collection_name, vector, filter,
    limit=vector_size)
  print('-----\nfilteredCollection: (' + str(len(filteredCollection)) + ')')
  print(filteredCollection)

main()