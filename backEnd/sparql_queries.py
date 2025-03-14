class InvolvedParty:
    SHIPPERNAME="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                    SELECT ?name 
                    WHERE { 
                        ?party a cargo:Party ; 
                        cargo:partyRole <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#SHP> ; 
                        cargo:partyDetails [ cargo:name ?name ] . 
                    }"""
    CONSIGNEENAME="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX code: <https://onerecord.iata.org/ns/code-lists/> 
                    SELECT ?name 
                    WHERE { 
                        ?party a cargo:Party ; 
                        cargo:partyRole <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#CNE> ; 
                        cargo:partyDetails [ cargo:name ?name ] .
                    }"""
