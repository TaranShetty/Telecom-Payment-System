def chatbot_reply(message, amounts, times):
    msg = message.lower()


    if "pgcil" in msg:
        if "pending" in msg or "amount" in msg:
            return f"PGCIL has a pending amount of ₹{amounts['pgcil']:.2f}."
        if "quarter" in msg or "period" in msg:
            return f"PGCIL has {times['pgcil']} quarters pending."
        return "PGCIL follows quarterly billing."

    if "jio" in msg:
        if "pending" in msg or "amount" in msg:
            return f"JIO has a pending amount of ₹{amounts['jio']:.2f}."
        if "quarter" in msg or "period" in msg:
            return f"JIO has {times['jio']} quarters pending."
        return "JIO follows quarterly billing."

    if "bsnl" in msg:
        if "pending" in msg or "amount" in msg:
            return f"BSNL has a pending amount of ₹{amounts['bsnl']:.2f}."
        if "half" in msg or "period" in msg:
            return f"BSNL has {times['bsnl']} half-year periods pending."
        return "BSNL follows half-yearly billing."


    if "highest" in msg or "maximum" in msg:
        vendor = max(amounts, key=amounts.get)
        return f"{vendor.upper()} has the highest pending amount of ₹{amounts[vendor]:.2f}."

    if "summary" in msg or "all vendors" in msg:
        return (
            f"Pending Summary:\n"
            f"PGCIL: ₹{amounts['pgcil']:.2f}\n"
            f"JIO: ₹{amounts['jio']:.2f}\n"
            f"BSNL: ₹{amounts['bsnl']:.2f}"
        )

  
    if "billing" in msg or "cycle" in msg:
        return (
            "Billing Cycles:\n"
            "• PGCIL – Quarterly\n"
            "• JIO – Quarterly\n"
            "• BSNL – Half-yearly"
        )

    return (
        "I can help you with:\n"
        "• Pending amount per vendor\n"
        "• Pending periods\n"
        "• Highest dues\n"
        "• Billing cycles\n"
        "Ask something like: 'PGCIL pending amount'"
    )
