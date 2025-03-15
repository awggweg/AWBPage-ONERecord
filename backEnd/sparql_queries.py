class InvolvedParty:
    shipper="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                PREFIX ParticipantIdentifier:  <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                SELECT ?Name ?Address 
                WHERE { 
                        ?waybill a cargo:Waybill.
                        ?waybill cargo:involvedParties [ 
                        <https://onerecord.iata.org/ns/cargo#partyRole>  ParticipantIdentifier:SHP ;
                        cargo:partyDetails [
                            cargo:name ?Name ;
                            cargo:basedAtLocation/cargo:locationName ?Address
                        ]
                    ]   
                }"""
    consinee="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name ?Address
                    WHERE { 
                            ?waybill cargo:involvedParties [ 
                            cargo:partyRole ParticipantIdentifier:CNE ;
                            cargo:partyDetails [
                                cargo:name ?Name ;
                                cargo:basedAtLocation/cargo:locationName ?Address
                            ]
                            ]
                    }"""
    airline="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name ?Airlinecode
                    WHERE { 
                            ?waybill cargo:involvedParties [ 
                            cargo:partyRole ParticipantIdentifier:AIR ;
                            cargo:partyDetails [
                                cargo:name ?Name ;
                                cargo:airlineCode ?Airlinecode
                            ]
                        ]
                    }"""
    
    carrierAgent="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#> 
                    PREFIX ParticipantIdentifier: <https://onerecord.iata.org/ns/code-lists/ParticipantIdentifier#>
                    SELECT ?Name
                    WHERE { 
                        ?waybill cargo:involvedParties [ 
                        cargo:partyRole ParticipantIdentifier:AGT ;
                        cargo:partyDetails [
                            cargo:name ?Name
                            ]
                        ]
                    }"""
    accountingInformation="""PREFIX cargo: <https://onerecord.iata.org/ns/cargo#>
                            SELECT ?accountingNoteText
                            WHERE { 
                                ?waybill cargo:accountingNotes [ 
                                cargo:accountingNoteText ?accountingNoteText ;
                                ]
                            }"""