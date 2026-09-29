# Networks, DNS and exposure

Open this file on a service-discovery question, a proxy misrouting, or any decision about which
port is reachable from where.

---

## 1. One shared network per family

When joining service families to a shared network, use [Network and DNS](./50-network-dns-and-exposure/10-network-and-dns.md).

## 2. Stable DNS: one name per HTTP backend

When resolving a stable HTTP backend DNS name, use [Network and DNS](./50-network-dns-and-exposure/10-network-and-dns.md).

## 3. Exposure, with a scope

When publishing a port and choosing its exposure scope, use [Exposure and forwarded trust](./50-network-dns-and-exposure/20-exposure-and-forwarded-trust.md).

## 4. Trust boundaries and forwarded headers

When trusting forwarded headers across a proxy boundary, use [Exposure and forwarded trust](./50-network-dns-and-exposure/20-exposure-and-forwarded-trust.md).

## 5. Diagnosing discovery and routing

When diagnosing service discovery or routing, use [Discovery diagnosis](./50-network-dns-and-exposure/30-discovery-diagnosis.md).
