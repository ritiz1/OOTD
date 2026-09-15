"""Outfit recommendation domain package.

The ADK agent is intentionally imported by the request handler only when a
recommendation is requested. This keeps unrelated wardrobe endpoints usable in
deployments that do not run the optional recommendation worker dependency.
"""
