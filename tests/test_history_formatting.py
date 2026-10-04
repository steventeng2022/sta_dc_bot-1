from bot.utils.history_formatting import build_embed
from bot.utils.history_today import Category, HistoryItem, HistoryResult, source_url


def test_history_embed_fits_limits_and_preserves_source_without_mentions():
    items = tuple(
        HistoryItem("2000年", "@everyone <@123456789012345678> **" + "很長的內容" * 200)
        for _ in range(10)
    )
    result = HistoryResult(10, 4, Category.EVENTS, items, source_url(10, 4))
    embed = build_embed(result, count=10)
    assert len(embed.description) <= 4096
    assert len(embed) <= 6000
    assert "@everyone" not in embed.description
    assert "<@123456789012345678>" not in embed.description
    assert embed.url == result.source_url
    assert "CC BY-SA" in embed.footer.text
    assert "…" in embed.description


def test_missing_category_data_has_readable_source_link():
    result = HistoryResult(2, 29, Category.HOLIDAYS, (), source_url(2, 29))
    embed = build_embed(result)
    assert "沒有列出" in embed.description
    assert result.source_url in embed.fields[0].value
