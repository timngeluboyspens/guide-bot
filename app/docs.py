api_docs = {
    'view_documents': {
        'tags': ['Document'],
        'summary': 'View documents or a specific document by ID',
        'description': 'Fetch one or all documents from the database. If an ID is provided, it fetches a specific document, otherwise returns a list of all documents.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': False,
                'type': 'string',
                'description': 'The ID of the document to fetch'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully fetched document(s)',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'description': 'Document ID'
                            },
                            'title': {
                                'type': 'string',
                                'description': 'Document title'
                            },
                            'created_at': {
                                'type': 'string',
                                'format': 'date-time',
                                'description': 'Document creation timestamp'
                            },
                            'updated_at': {
                                'type': 'string',
                                'format': 'date-time',
                                'description': 'Document last update timestamp'
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'Document not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Document not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while fetching document(s)',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while fetching the documents'
                        }
                    }
                }
            }
        }
    },    

    'create_document': {
        'tags': ['Document'],
        'summary': 'Create a new document',
        'description': 'Upload a document file and save it in the database.',
        'consumes': ['multipart/form-data'],
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'required': True,
                'type': 'file',
                'description': 'The document file to upload'
            }
        ],
        'responses': {
            '201': {
                'description': 'Document successfully created',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'description': 'Document ID'
                        },
                        'title': {
                            'type': 'string',
                            'description': 'Document title (filename)'
                        },
                        'created_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Document creation timestamp'
                        },
                        'updated_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Document last update timestamp'
                        }
                    }
                }
            },
            '400': {
                'description': 'Invalid input - file not provided or file name invalid',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'File is required'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while creating the document',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while creating the document'
                        }
                    }
                }
            }
        }
    },

    'update_document': {
        'tags': ['Document'],
        'summary': 'Update a specific document by ID',
        'description': 'Update the file and/or title of a specific document in the database by providing its ID.',
        'consumes': ['multipart/form-data'],
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'The ID of the document to update'
            },
            {
                'name': 'file',
                'in': 'formData',
                'required': False,
                'type': 'file',
                'description': 'The new file to update the document with'
            }
        ],
        'responses': {
            '200': {
                'description': 'Document successfully updated',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'description': 'Document ID'
                        },
                        'title': {
                            'type': 'string',
                            'description': 'Document title'
                        },
                        'created_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Document creation timestamp'
                        },
                        'updated_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Document last update timestamp'
                        }
                    }
                }
            },
            '404': {
                'description': 'Document not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Document not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while updating the document',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while updating document with ID {id}'
                        }
                    }
                }
            }
        }
    },

    'delete_document': {
        'tags': ['Document'],
        'summary': 'Delete a specific document by ID',
        'description': 'Delete a document from the database by providing its ID.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'The ID of the document to delete'
            }
        ],
        'responses': {
            '200': {
                'description': 'Document successfully deleted',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Document deleted successfully'
                        }
                    }
                }
            },
            '404': {
                'description': 'Document not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Document not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while deleting the document',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while deleting document with ID {id}'
                        }
                    }
                }
            }
        }
    },   

    'view_conversations': {
        'tags': ['Conversation'],
        'summary': 'View all conversations or a specific conversation by ID',
        'description': 'Fetches all conversations or a specific conversation based on the provided conversation ID. If no ID is provided, returns all conversations.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': False,
                'type': 'string',
                'description': 'The ID of the conversation to fetch'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully fetched conversation(s)',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'string',
                                'description': 'Conversation ID'
                            },
                            'title': {
                                'type': 'string',
                                'description': 'Conversation title'
                            },
                            'created_at': {
                                'type': 'string',
                                'format': 'date-time',
                                'description': 'Conversation creation timestamp'
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'Conversation not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Conversation not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while fetching conversation(s)',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while fetching the conversations'
                        }
                    }
                }
            }
        }
    },

    'create_conversation': {
        'tags': ['Conversation'],
        'summary': 'Create a new conversation',
        'description': 'Creates a new conversation in the database with a title and associates it with the user ID from request headers.',
        'parameters': [
            {
                'name': 'Authorization',
                'in': 'header',
                'required': True,
                'type': 'string',
                'description': 'The ID of the user creating the conversation'
            },
            {
                'name': 'title',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'The title of the conversation'
                        }
                    }
                }
            }
        ],
        'responses': {
            '201': {
                'description': 'Successfully created conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                            'description': 'Conversation ID'
                        },
                        'title': {
                            'type': 'string',
                            'description': 'Conversation title'
                        },
                        'created_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Conversation creation timestamp'
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad request (e.g., missing required fields)',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'User ID or conversation title is required'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while creating conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while creating the conversation'
                        }
                    }
                }
            }
        }
    },

    'update_conversation': {
        'tags': ['Conversation'],
        'summary': 'Update a conversation by ID',
        'description': 'Updates the title of a conversation based on the provided conversation ID.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'The ID of the conversation to update'
            },
            {
                'name': 'title',
                'in': 'body',
                'required': False,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'New title of the conversation'
                        }
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully updated conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                            'description': 'Conversation ID'
                        },
                        'title': {
                            'type': 'string',
                            'description': 'Conversation title'
                        },
                        'created_at': {
                            'type': 'string',
                            'format': 'date-time',
                            'description': 'Conversation creation timestamp'
                        }
                    }
                }
            },
            '404': {
                'description': 'Conversation not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Conversation not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while updating conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while updating conversation with ID {conversation_id}'
                        }
                    }
                }
            }
        }
    },

    'delete_conversation': {
        'tags': ['Conversation'],
        'summary': 'Delete a conversation by ID',
        'description': 'Deletes a conversation from the database based on the provided conversation ID.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'The ID of the conversation to delete'
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully deleted conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Conversation deleted successfully'
                        }
                    }
                }
            },
            '404': {
                'description': 'Conversation not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Conversation not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while deleting conversation',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred while deleting conversation with ID {conversation_id}'
                        }
                    }
                }
            }
        }
    },

    'chat': {
        'tags': ['Conversation'],
        'summary': 'Send a message to a conversation',
        'description': 'Sends a message from a user to an existing conversation and processes a chatbot response.',
        'parameters': [
            {
                'name': 'Authorization',
                'in': 'header',
                'required': True,
                'type': 'string',
                'description': 'The ID of the user sending the message'                                
            },
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'The ID of the conversation to send the message to'
            },
            {
                'name': 'user_input',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'user_input': {
                            'type': 'string',
                            'description': 'Message from the user to send'
                        }
                    }
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Successfully processed chatbot response',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'response': {
                            'type': 'string',
                            'description': 'Response message from the chatbot'
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad request (e.g., missing user input or session mismatch)',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'User input or session is required'
                        }
                    }
                }
            },
            '404': {
                'description': 'Conversation not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Conversation not found'
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error while processing chat',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'An error occurred during the chat process'
                        }
                    }
                }
            }
        }
    },
 
    'reload_vector_db' : {
        'tags': ['Document'],   
        'summary': 'Reload Vector Database',
        'description': 'Reload the vector database with the latest data from the documents.',
        'responses': {
            '200': {
                'description': 'Vector database reloaded successfully'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    
}