from neomodel import StructuredNode, StringProperty, RelationshipTo, OneOrMore, RelationshipFrom, One, ZeroOrMore

__author__ = 'naman'

class Photos(StructuredNode):
    name=StringProperty(unique_index=True,required=True)
    uploaded=RelationshipFrom('User','Uploader',One)

class User(StructuredNode):
    name=StringProperty(unique_index=True,required=True)
    uploader=RelationshipFrom('Photos','Uploaded',OneOrMore)
    friend_req=RelationshipTo('User','Request',ZeroOrMore)
    currentdp=RelationshipTo('Photos','Dp',One)

    def getAllImages(self):
        query = 'START a=node({self}) match (a)-[:Uploader]->(b:Photos) return b'
        results, columns = self.cypher(query)
        #Declare a List and then populate it with results
        maleList = []
        for row in results:
            maleList.append(self.inflate(row[0]))
        return maleList
