# Security Policy

Do not commit credentials, access tokens, private keys, `.env` files, customer
data, employer source code, or confidential take-home material.

The CLI rejects target repositories located inside configured protected paths
when a project policy forbids them. Project profiles should also define secret
path markers and network-access policy.
