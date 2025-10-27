from abc import ABC, abstractmethod

class baseRecord(ABC):

    @abstractmethod
    @staticmethod
    def fromDict()
        pass
    @abstractmethod
    def toDict()
        pass

class baseOperations(ABC):
    def __init__(self, person):
        self.person=person
        
    def addRecord(content)
        if self.person.position == "manager":
            table=self.type+"_public"
        else:
            table=self.type+"_private"

        joke=self.record.fromdict(content)
        jokeDict=joke.todict()

        dao.add(table, self.person, jokeDict)
    
    def deleteRecord(id):
        if self.person.title =="manager":
            table=self.type+"_public"
            dao.delete(table,self.person,id)

    def updateRecord(id,content):
        if self.person.title =="manager":
            table=self.type+"_public"
            dao.update(table,id,content,person)
        else:
            table=self.type+"_private"
            (change content to have id and isedit)
            dao.add(table,content,person)
    
    def queryRecords(filters):

    def approveDenyRecord(id,approve):
        if self.person.title =="manager":
            table=self.type+"_private"
            if approve==True:
                content=dao.get(table,id)
                if content["isEdit"] ==True:
                    dao.update(table,content["refID"],content,person )
                else:
                    dao.add(table,content,person)
            else:
                dao.delete(table,id)

    
content={"joke":"Haha","difficulty":1}

class jokeRecord():
    def __init__(self, joke, difficulty):
        #set business logic rules here
        self.joke=joke
        self.difficulty=difficulty

    @staticmethod
    def fromdict(content):
        return jokeRecord(content["joke"],content["difficulty"])
    
    def todict(self):
        return {"joke":self.joke, "difficulty":self.difficulty}
    

print(jokeRecord.fromdict(content).joke)

class jokeOperations():
    def __init__(self, person):
        self.person=person
        self.type="joke"
        self.record=jokeRecord

    def add(content):
        if self.person.position == "manager":
            table=self.type+"_public"
        else:
            table=self.type+"_private"

        joke=self.record.fromdict(content)
        jokeDict=joke.todict()

        dao.add(table, self.person, jokeDict)
