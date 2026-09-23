# Network Crawlers

The network crawlers collect peer-to-peer topology data from the Gnosis Chain network. Two services work together: **nebula** discovers peers by crawling the DHT, and **ip-crawler** enriches those peers with geolocation data.

## Components

| Crawler | Language | Purpose | Target Database |
|---------|----------|---------|-----------------|
| [nebula](nebula.md) | Go | DHT crawling, peer discovery, client metadata collection — one crawler per network (discv5 and discv4) | `nebula`, `nebula_discv4` |
| [ip-crawler](ip-crawler.md) | Python | IP geolocation enrichment via ipinfo.io, daily; feeds three public-dashboard HOPR marts | `crawlers_data` |

Neither crawler has an alert rule. Health is a data query — see each page's **Operating and recovering** section.

## Data Flow

```
Gnosis Chain P2P Network
        |
        v
    nebula (DHT Crawler)
        |
        v
  nebula.visits table
  (peer IPs, agent versions, fork digests)
        |
        v
    ip-crawler
        |
        v
  crawlers_data.ipinfo table
  (city, country, ASN, organization)
        |
        v
    dbt-cerebro (p2p module)
        |
        v
  Peer distribution analytics, geographic heatmaps,
  client version statistics, network health metrics
```

## Downstream Usage

The data collected by these crawlers feeds into the **p2p** module in dbt-cerebro, which produces analytics including:

- Geographic distribution of Gnosis Chain nodes
- Client version adoption and diversity metrics
- Network topology analysis
- Peer reachability statistics
