api_docs = {
    'view_documents': {
        'summary': 'View Documents',
        'description': 'Retrieve a list of all documents or a specific document by ID.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': False,
                'description': 'The ID of the document',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Success',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'string'},
                                    'title': {'type': 'string'},
                                    'created_at': {'type': 'string'},
                                    'updated_at': {'type': 'string'}
                                }
                            }
                        }
                    }
                }
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'create_document': {
        'summary': 'Create a Document',
        'description': 'Upload a document and store it in the system.',
        'requestBody': {
            'required': True,
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'file': {
                                'type': 'string',
                                'format': 'binary'
                            }
                        }
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Document created successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'title': {'type': 'string'},
                                'created_at': {'type': 'string'},
                                'updated_at': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'update_document': {
        'summary': 'Update a Document',
        'description': 'Update the file or title of an existing document.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the document to update',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'file': {
                                'type': 'string',
                                'format': 'binary'
                            }
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {
                'description': 'Document updated successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'title': {'type': 'string'},
                                'created_at': {'type': 'string'},
                                'updated_at': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'delete_document': {
        'summary': 'Delete a Document',
        'description': 'Delete a document by its ID.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the document to delete',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Document deleted successfully'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'view_conversations': {
        'summary': 'View Conversations',
        'description': 'Retrieve a list of all conversations or a specific conversation by ID.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': False,
                'description': 'The ID of the conversation',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Success',
                'content': {
                    'application/json': {
                        'oneOf': [
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'string'},
                                        'title': {'type': 'string'},
                                        'created_at': {'type': 'string'},
                                        'updated_at': {'type': 'string'}
                                    }
                                },
                                'description': 'List of all conversations'
                            },
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'conversation_id': {'type': 'string'},
                                        'messages': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {'type': 'string'},
                                                    'message': {'type': 'string'},
                                                    'sender': {'type': 'string'},
                                                    'created_at': {'type': 'string'},
                                                }
                                            }
                                        }
                                    }
                                },
                                'description': 'List of messages for a specific conversation'
                            }
                        ]
                    }
                }
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'create_conversation': {
        'summary': 'Create a Conversation',
        'description': 'Create a new conversation.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': 'Title of the conversation'
                            },
                            'user_id': {
                                'type': 'string',
                                'description': 'User ID'
                            }
                        },
                        'required': ['title', 'user_id']
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'Conversation created successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'title': {'type': 'string'},
                                'created_at': {'type': 'string'},
                                'updated_at': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'update_conversation': {
        'summary': 'Update a Conversation',
        'description': 'Update the title of an existing conversation.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the conversation to update',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'title': {
                                'type': 'string',
                                'description': 'New title for the conversation'
                            }
                        }
                    }
                }
            }
        },
        'responses': {
            '200': {
                'description': 'Conversation updated successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'title': {'type': 'string'},
                                'created_at': {'type': 'string'},
                                'updated_at': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'delete_conversation': {
        'summary': 'Delete a Conversation',
        'description': 'Delete a conversation by its ID.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the conversation to delete',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Conversation deleted successfully'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'chat': {
        'summary': 'Chat',
        'description': 'Send a user input to the chatbot and get a response.',
        'parameters': [
            {
                'name': 'conversation_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the conversation',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'user_input': {
                                'type': 'string',
                                'description': 'Input message from the user'
                            }
                        },
                        'required': ['user_input']
                    }
                }
            }
        },
        'responses': {
            '200': {
                'description': 'Chat response',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'response': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '404': {
                'description': 'Conversation not found'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    },
    'reload_vector_db' : {
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
    'user_session' : {
        'summary': 'User Session',
        'description': 'Create a new user session.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'user_id': {
                                'type': 'string',
                                'description': 'User ID'
                            }
                        },
                        'required': ['user_id']
                    }
                }
            }
        },
        'responses': {
            '201': {
                'description': 'User session created successfully',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'conversation_id': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad Request'
            },
            '500': {
                'description': 'Internal server error'
            }
        }
    }
}