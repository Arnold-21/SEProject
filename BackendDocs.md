# Backend Documentation

## Base_URL:   -- SE-Backend.strangled.net --



1. 'api/token/'
    - Given the username and password gives back an access and refresh token, which is used for authentication
    - POST method
        - body: {
            email: string,
            password: string
        }
        - response: {
            access: string,
            refresh: string
        }
        - error-Response: {
            detail: string
        }
2. 'api/token/refresh/'
    - Given the refresh token, it generates a new refresh and access token
    - POST method
        - body: {
            refresh: string
        }
        - response: {
            access: string
            refresh: string
        }
        - error-Response: {
            detail: string
        }
3. 'api/register/'
    - Given the neccessary information, it generates an inactive account, in response, the id of that user and sends an email to the user with the confirmation code
    - POST method
        - body: {
            first_name: string
            last_name: string
            password: string
            email: string
        }
        - response: {
            success: int
        }
        - error-Response: {
            error: string
        }
4. 'api/register/confirm/<int:code>/<int:id>/'
    - The code and user id given, in the url, if it matches, the account will be activated
    - GET method
        - response: {
            success: string
        }
        - error-Response: {
            error: string
        }
5. 'api/user/<int:id>/'
    - The user given in the url, allows operations on a specific user
    - header: {
        Authorization: "Bearer "  + (access token)
    }
        - GET method
            - response: {
                id: int
                last_name: string
                first_name: string
                email: string
            }
            - error-Response: {
                error: string / detail: string
            }
        - PUT method
            - body: { (optional values)
                first_name: string
                last_name: string
                password: string
                email: string
            }
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
        - DELETE method
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
6. 'api/recover/'
    - Given an email, if a user is present, it generates a code (sent via email to the user), which is used later to recover the account
    - POST method
        - body: {
            email: string
        }
        - response: {
            success: id (user id)
        }
        - error-Response: {
            error: string / detail: string
        }
7. 'api/recover/<int:code>/<int:id>/'
    - The user id and the recovery code sent via email, given in the url, the new password in the body, changes the user password, if the id and recovery code doesn't match, it gives back an error
    - PUT method
        - body: {
            password: string
        }
        - response: {
            success: string
        }
        - error-Response: {
            error: string / detail: string
        }
8. 'api/privatelist/'
    - Given permission, it returns back the users private bucket list, or the user can add a new destination
    - header: {
        Authorization: "Bearer "  + (access token)
    }
        - GET method
            - response: {
                [
                    {
                        "id": int,
                        "location": {
                            "id": int,
                            "country": string,
                            "county": string,
                            "settlement": string,
                            "street": string,
                            "number": itn
                        },
                        "title": string,
                        "description": string,
                        "arrivalDate": string,
                        "leaveDate": string,
                        "image": string,
                        "isPublic": boolean,
                        "userID": int
                    }
                ]
            }
            - error-Response: {
                error: string / detail: string
            }
        - POST method (Has to be a FormData in javascript)
            - body: {
                "country": string,
                "county": string,
                "settlement": string,
                "street": string,
                "number": int (= street number)
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": file,
                "userID": int
            }
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
9. 'api/privatelist/<int:id>/'
    - Allows specific operations on the destination given by id
    - header: {
        Authorization: "Bearer "  + (access token)
    }
        - GET method
            - response: {
                "id": int,
                "location": {
                    "id": int,
                    "country": string,
                    "county": string,
                    "settlement": string,
                    "street": string,
                    "number": itn
                },
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": string,
                "isPublic": boolean,
                "userID": int
            }
            - error-Response: {
                error: string / detail: string
            }
        - PUT method
            - body: { (optinal values)
                "country": string,
                "county": string,
                "settlement": string,
                "street": string,
                "number": int (= street number)
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": file,
                "userID": int
            }
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
        - DELETE method
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
10. 'api/privatelist/public/<int:id>/'
    - Given the destination id and neccessary permission, the destination is put public
    - PUT method
        - header: {
            Authorization: "Bearer "  + (access token)
        }
        - response: {
            success: string
        }
        - error-Response: {
            error: string / detail: string
        }
11. path('api/publiclist/', PublicListView.as_view()),
    - Retrieves the public destinations
    - GET method
        - response: [{
            "id": int,
            "location": {
                "id": int,
                "country": string,
                "county": string,
                "settlement": string,
                "street": string,
                "number": int
            },
            "title": string,
            "description": string,
            "arrivalDate": string,
            "leaveDate": string,
            "image": string,
            "isPublic": boolean,
            "userID": int
        }]
        - error-Response: {
            error: string / detail: string
        }
12. 'api/admin/publiclist/'
    - Given permission, it returns back the public list, or the admin can add a new destination
    - header: {
        Authorization: "Bearer "  + (access token)
    }
        - GET method
            - response: {
                [
                    {
                        "id": int,
                        "location": {
                            "id": int,
                            "country": string,
                            "county": string,
                            "settlement": string,
                            "street": string,
                            "number": itn
                        },
                        "title": string,
                        "description": string,
                        "arrivalDate": string,
                        "leaveDate": string,
                        "image": string,
                        "isPublic": boolean,
                        "userID": int
                    }
                ]
            }
            - error-Response: {
                error: string / detail: string
            }
        - POST method (Has to be a FormData in javascript)
            - body: {
                "country": string,
                "county": string,
                "settlement": string,
                "street": string,
                "number": int (= street number)
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": file,
                "isPublic": boolean,
                "userID": int
            }
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
13. 'api/admin/publiclist/<int:id>/'
    - Allows specific operations on the destination given by id and admin permission
    - header: {
        Authorization: "Bearer "  + (access token)
    }
        - GET method
            - response: {
                "id": int,
                "location": {
                    "id": int,
                    "country": string,
                    "county": string,
                    "settlement": string,
                    "street": string,
                    "number": itn
                },
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": string,
                "isPublic": boolean,
                "userID": int
            }
            - error-Response: {
                error: string / detail: string
            }
        - PUT method
            - body: { (optinal values)
                "country": string,
                "county": string,
                "settlement": string,
                "street": string,
                "number": int (= street number)
                "title": string,
                "description": string,
                "arrivalDate": string,
                "leaveDate": string,
                "image": file,
                "userID": int
            }
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }
        - DELETE method
            - response: {
                success: string
            }
            - error-Response: {
                error: string / detail: string
            }