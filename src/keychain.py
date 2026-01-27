"""
OS keychain integration for secure credential storage.

This module provides functions for storing, retrieving, and managing
API keys and other credentials using the platform's native keyring service.
"""

import keyring
import keyring.errors
import json
from typing import Dict, Optional
from .exceptions import (
    KeyNotFoundError,
    KeychainAccessError,
    KeychainStorageError,
    KeychainDeletionError,
    InvalidKeyNameError,
    ValidationError
)

SERVICE_NAME = "backpack-agent"

def _validate_key_name(key_name: str) -> None:
    """
    Validate a key name.
    
    Args:
        key_name: The key name to validate
    
    Raises:
        InvalidKeyNameError: If the key name is invalid
    """
    if not key_name:
        raise InvalidKeyNameError("", "Key name cannot be empty")
    
    if not isinstance(key_name, str):
        raise InvalidKeyNameError(
            str(key_name),
            f"Key name must be a string, got {type(key_name).__name__}"
        )
    
    # Key names should not start with underscore (reserved for internal use)
    # except for the registry key
    if key_name.startswith('_') and key_name != '_registry':
        raise InvalidKeyNameError(
            key_name,
            "Key names starting with '_' are reserved for internal use"
        )


def store_key(key_name: str, key_value: str) -> None:
    """
    Store a key-value pair in the OS keychain.
    
    Args:
        key_name: The name/identifier of the key
        key_value: The secret value to store
    
    Raises:
        InvalidKeyNameError: If key_name is invalid
        KeychainStorageError: If storing the key fails
    """
    _validate_key_name(key_name)
    
    if key_value is None:
        raise ValidationError(
            "Key value cannot be None",
            "Provide a valid string value to store"
        )
    
    if not isinstance(key_value, str):
        raise ValidationError(
            "Key value must be a string",
            f"Got type: {type(key_value).__name__}"
        )
    
    try:
        keyring.set_password(SERVICE_NAME, key_name, key_value)
    except keyring.errors.KeyringError as e:
        raise KeychainStorageError(
            key_name,
            f"Keyring error: {str(e)}"
        ) from e
    except Exception as e:
        raise KeychainStorageError(
            key_name,
            f"Unexpected error: {str(e)}"
        ) from e

def get_key(key_name: str) -> Optional[str]:
    """
    Retrieve a key value from the OS keychain.
    
    Args:
        key_name: The name/identifier of the key to retrieve
    
    Returns:
        The stored key value, or None if not found
    
    Raises:
        InvalidKeyNameError: If key_name is invalid
        KeychainAccessError: If accessing the keychain fails
    """
    _validate_key_name(key_name)
    
    try:
        return keyring.get_password(SERVICE_NAME, key_name)
    except keyring.errors.KeyringError as e:
        raise KeychainAccessError(
            f"Failed to retrieve key '{key_name}' from keychain",
            str(e)
        ) from e
    except Exception as e:
        raise KeychainAccessError(
            f"Unexpected error retrieving key '{key_name}'",
            str(e)
        ) from e

def list_keys() -> Dict[str, bool]:
    """
    List all keys registered in the keychain.
    
    Note: The OS keyring doesn't provide native list functionality,
    so we maintain a registry of keys.
    
    Returns:
        A dictionary mapping key names to True (indicating they exist)
    
    Raises:
        KeychainAccessError: If accessing the keychain fails
    """
    try:
        # Note: keyring doesn't provide list functionality, so we maintain a registry
        registry = get_key("_registry")
        if registry:
            try:
                return json.loads(registry)
            except json.JSONDecodeError as e:
                # Registry is corrupted, return empty dict
                return {}
        return {}
    except KeychainAccessError:
        # If we can't access the registry, return empty dict
        # This is not a critical error - the registry might not exist yet
        return {}

def register_key(key_name: str) -> None:
    """
    Register a key name in the keychain registry.
    
    This is used to track which keys exist, since the OS keyring
    doesn't provide native list functionality.
    
    Args:
        key_name: The name of the key to register
    
    Raises:
        InvalidKeyNameError: If key_name is invalid
        KeychainStorageError: If storing the registry fails
    """
    _validate_key_name(key_name)
    
    try:
        registry = list_keys()
        registry[key_name] = True
        keyring.set_password(SERVICE_NAME, "_registry", json.dumps(registry))
    except (KeychainAccessError, KeychainStorageError):
        # If registry operations fail, we can still continue
        # The key itself was already stored successfully
        pass
    except Exception as e:
        raise KeychainStorageError(
            "_registry",
            f"Failed to update registry: {str(e)}"
        ) from e

def delete_key(key_name: str) -> None:
    """
    Delete a key from the keychain and registry.
    
    Args:
        key_name: The name of the key to delete
    
    Raises:
        InvalidKeyNameError: If key_name is invalid
        KeyNotFoundError: If the key doesn't exist
        KeychainDeletionError: If deletion fails
    """
    _validate_key_name(key_name)
    
    # Check if key exists first
    existing_key = get_key(key_name)
    if existing_key is None:
        raise KeyNotFoundError(key_name)
    
    try:
        keyring.delete_password(SERVICE_NAME, key_name)
    except keyring.errors.PasswordDeleteError as e:
        raise KeychainDeletionError(
            key_name,
            f"Keyring deletion error: {str(e)}"
        ) from e
    except keyring.errors.KeyringError as e:
        raise KeychainDeletionError(
            key_name,
            f"Keyring error: {str(e)}"
        ) from e
    except Exception as e:
        raise KeychainDeletionError(
            key_name,
            f"Unexpected error: {str(e)}"
        ) from e
    
    # Update registry
    try:
        registry = list_keys()
        registry.pop(key_name, None)
        keyring.set_password(SERVICE_NAME, "_registry", json.dumps(registry))
    except Exception:
        # Registry update failure is not critical - the key is already deleted
        pass