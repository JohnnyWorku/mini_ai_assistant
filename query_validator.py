from pydantic import BaseModel, Field, field_validator, ConfigDict

class CypherQuery(BaseModel):
    # to forbid any fields except the already defined one (cypher)
    model_config = ConfigDict(extra="forbid")
    
    cypher: str = Field(
        ...,
        description="A valid and safe Neo4j Cypher query"
    )
    
    
    @field_validator("cypher")
    @classmethod
    def validate_query(cls, value: str):
        
        # remove markdown if there
        value = value.replace("```cypher", "")
        value = value.replace("```", "")
        value = value.strip()
        
        
        if not value:
            raise ValueError("Cypher query cannot be empty")
        
        forbidden = [
            "DELETE",
            "DETACH DELETE",
            "CREATE",
            "MERGE",
            "DROP",
            "SET",
            "REMOVE",
            "LOAD CSV"
        ]
        
        upper = value.upper()
        
        for word in forbidden:
            if word in upper:
                raise ValueError(f"Dangerous operation detected: {word}")
            
        return value
