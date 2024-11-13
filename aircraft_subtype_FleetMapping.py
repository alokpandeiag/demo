
from sqlalchemy import Column, String, PrimaryKeyConstraint, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class FlightCrewAircraftFleetMapping(Base):
    __tablename__ = 'FLIGHTCREW_AIRCRAFT_FLEET_MAPPING'
    __table_args__ = (
        PrimaryKeyConstraint('AIRCRAFT_OWNER', 'AIRCRAFT_SUBTYPE', 'EFFECTIVE_FROM_DATETIME', 'EFFECTIVE_TO_DATETIME'),
        {'schema': 'iflightneoint'}  # Correct the schema name here if necessary
    )
    
 
    AIRCRAFT_OWNER = Column(String(3), primary_key=True, nullable=False)
    FLIGHT_CREW_LICENSE_FLEET = Column(String(4), nullable=True)
    FLIGHT_CREW_BASE_FLEET = Column(String(4), nullable=True)
    BA_QUALIFIED_FLEET =  Column(String(4), nullable=True)
    AIRCRAFT_TYPE_IATA = Column(String(3), nullable=False)
    AIRCRAFT_TYPE_ICAO = Column(String(4), nullable=True)
    AIRCRAFT_SUBTYPE = Column(String(3), primary_key=True, nullable=False)
    AIRCRAFT_SUBTYPE_ICAO = Column(String(4), nullable=True)
    FLEET_CODE_FICO_CONSOLIDATED = Column(String(8), nullable=True)
    EFFECTIVE_FROM_DATETIME = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    EFFECTIVE_TO_DATETIME = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)


    def __repr__(self):
        return (
            f"<FlightCrewAircraftFleetMapping(AIRCRAFT_OWNER='{self.AIRCRAFT_OWNER}', "
            f"AIRCRAFT_SUBTYPE='{self.AIRCRAFT_SUBTYPE}', "
            f"FLIGHT_CREW_LICENSE_FLEET='{self.FLIGHT_CREW_LICENSE_FLEET}', "
            f"FLIGHT_CREW_BASE_FLEET='{self.FLIGHT_CREW_BASE_FLEET}', "
            f"BA_QUALIFIED_FLEET='{self.BA_QUALIFIED_FLEET}', "
            f"AIRCRAFT_TYPE_IATA='{self.AIRCRAFT_TYPE_IATA}', "
            f"AIRCRAFT_TYPE_ICAO='{self.AIRCRAFT_TYPE_ICAO}', "
            f"AIRCRAFT_SUBTYPE_ICAO='{self.AIRCRAFT_SUBTYPE_ICAO}', "
            f"FLEET_CODE_FICO_CONSOLIDATED='{self.FLEET_CODE_FICO_CONSOLIDATED}', "
            f"EFFECTIVE_FROM_DATETIME='{self.EFFECTIVE_FROM_DATETIME}', "
            f"EFFECTIVE_TO_DATETIME='{self.EFFECTIVE_TO_DATETIME}')>"
        )