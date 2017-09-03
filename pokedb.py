import sqlite3

class PokeSQL:
    
    def __init__(self, cursor):
        self.c = cursor
    
    def dexNum(self, name):
        
        t = (name,)
        q = self.c.execute('SELECT pokemon_species_id \
                      FROM pokemon_species_names \
                      WHERE LOWER(name)=LOWER(?) \
                      AND local_language_id=9', t)
        r = q.fetchall()
        if len(r) == 0:
            return -1
        return r[0][0]
    
    
    def moveNum(self, name):
        
        t = (name,)
        q = self.c.execute('SELECT move_id \
                      FROM move_names \
                      WHERE LOWER(name)=LOWER(?) \
                      AND local_language_id=9', t)
        r = q.fetchall()
        if len(r) == 0:
            return -1
        return r[0][0]
    
    def typeNum(self, name):
        
        t = (name,)
        q = self.c.execute('SELECT type_id \
                      FROM type_names \
                      WHERE LOWER(name)=LOWER(?) \
                      AND local_language_id=9', t)
        r = q.fetchall()
        if len(r) == 0:
            return -1
        return r[0][0]
    
    
    def abilityNum(self, name):
        
        t = (name,)
        q = self.c.execute('SELECT ability_id \
                      FROM ability_names \
                      WHERE LOWER(name)=LOWER(?) \
                      AND local_language_id=9', t)
        r = q.fetchall()
        if len(r) == 0:
            return -1
        return r[0][0]
    
    def movePool(self, p_id, lv=100):
        
        t = (p_id,lv)
        res = []
        q = self.c.execute('SELECT M.move_id, N.name, M.level \
                      FROM pokemon_moves M \
                      JOIN move_names N ON M.move_id = N.move_id \
                      WHERE M.pokemon_id=? \
                      AND M.version_group_id=16\
                      AND M.level<=?\
                      AND M.pokemon_move_method_id=1\
                      AND N.local_language_id=9\
                      ORDER BY M.level', t)
        for row in q:
            res.append(row)
        return res
    
    def learnSet(self, p_id, lv=100):
        
        t = (p_id,lv)
        res = []
        q = self.c.execute('SELECT M.pokemon_id, N.name, M.level \
                      FROM pokemon_moves M \
                      JOIN pokemon_species_names N ON M.pokemon_id = N.pokemon_species_id \
                      WHERE M.move_id=? \
                      AND M.version_group_id=16\
                      AND M.level<=?\
                      AND M.pokemon_id<=493\
                      AND M.pokemon_move_method_id=1\
                      AND N.local_language_id=9\
                      ORDER BY M.pokemon_id', t)
        for row in q:
            if len(res) > 0 and row[0] == res[-1][0]:
                res[-1][2].append(row[2])
            else:
                res.append((row[0], row[1], [row[2]]))
        return res
    
    
    def abilityPool(self, p_id):
        
        t = (p_id,)
        res = []
        q = self.c.execute('SELECT M.ability_id, N.name, M.is_hidden \
                      FROM pokemon_abilities M \
                      JOIN ability_names N ON M.ability_id = N.ability_id \
                      WHERE M.pokemon_id=? \
                      AND N.local_language_id=9\
                      ORDER BY M.is_hidden', t)
        for row in q:
            res.append(row)
        return res
    
    def abilitySet(self, p_id):
        
        t = (p_id,)
        res = []
        q = self.c.execute('SELECT M.pokemon_id, N.name, M.is_hidden \
                      FROM pokemon_abilities M \
                      JOIN pokemon_species_names N ON M.pokemon_id = N.pokemon_species_id \
                      WHERE M.ability_id=? \
                      AND M.pokemon_id<=493\
                      AND N.local_language_id=9\
                      ORDER BY M.pokemon_id', t)
        for row in q:
            res.append(row)
        return res
    
    def typeSet(self, p_id):
        
        t = (p_id,)
        res = []
        q = self.c.execute('SELECT M.pokemon_id, N.name \
                      FROM pokemon_types M \
                      JOIN pokemon_species_names N ON M.pokemon_id = N.pokemon_species_id \
                      WHERE M.type_id=? \
                      AND M.pokemon_id<=493\
                      AND N.local_language_id=9\
                      ORDER BY M.pokemon_id', t)
        for row in q:
            res.append(row)
        return res

# conn = sqlite3.connect('pokedex.sqlite')        
# c = conn.cursor()
# db = PokeSQL(c)
# ret = db.typeSet(db.typeNum("dragon"))
# print(ret)
