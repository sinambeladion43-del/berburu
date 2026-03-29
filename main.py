import logging
import asyncio
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler
)
from config.settings import BOT_TOKEN, ADMIN_IDS
from handlers import (
    start, hunt, market, home, museum,
    weapons, inventory, profile, leaderboard
)
from admin import (
    dashboard, manage_content, economy,
    players, events, transactions, bot_settings, logs, roles
)
from database.db import init_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    await init_db()
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # === USER HANDLERS ===
    app.add_handler(CommandHandler("start", start.cmd_start))
    app.add_handler(CommandHandler("help", start.cmd_help))
    
    # Main menu callbacks
    app.add_handler(CallbackQueryHandler(start.main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(hunt.menu_hunt, pattern="^menu_hunt$"))
    app.add_handler(CallbackQueryHandler(market.menu_market, pattern="^menu_market$"))
    app.add_handler(CallbackQueryHandler(home.menu_home, pattern="^menu_home$"))
    app.add_handler(CallbackQueryHandler(museum.menu_museum, pattern="^menu_museum$"))
    app.add_handler(CallbackQueryHandler(weapons.menu_weapons, pattern="^menu_weapons$"))
    app.add_handler(CallbackQueryHandler(inventory.menu_inventory, pattern="^menu_inventory$"))
    app.add_handler(CallbackQueryHandler(profile.menu_profile, pattern="^menu_profile$"))
    app.add_handler(CallbackQueryHandler(leaderboard.menu_leaderboard, pattern="^menu_leaderboard$"))
    
    # Hunt callbacks
    app.add_handler(CallbackQueryHandler(hunt.select_map, pattern="^map_"))
    app.add_handler(CallbackQueryHandler(hunt.select_animal, pattern="^hunt_animal_"))
    app.add_handler(CallbackQueryHandler(hunt.do_hunt, pattern="^do_hunt_"))
    app.add_handler(CallbackQueryHandler(hunt.filter_rarity, pattern="^filter_rarity_"))
    app.add_handler(CallbackQueryHandler(hunt.search_animal, pattern="^search_animal$"))
    
    # Market callbacks
    app.add_handler(CallbackQueryHandler(market.sell_inventory, pattern="^market_sell$"))
    app.add_handler(CallbackQueryHandler(market.sell_item, pattern="^sell_item_"))
    app.add_handler(CallbackQueryHandler(market.check_prices, pattern="^market_prices$"))
    app.add_handler(CallbackQueryHandler(market.p2p_market, pattern="^market_p2p$"))
    app.add_handler(CallbackQueryHandler(market.p2p_buy, pattern="^p2p_buy_"))
    app.add_handler(CallbackQueryHandler(market.p2p_list, pattern="^p2p_list$"))
    app.add_handler(CallbackQueryHandler(market.p2p_create, pattern="^p2p_create$"))
    
    # Home callbacks
    app.add_handler(CallbackQueryHandler(home.eat_food, pattern="^eat_"))
    app.add_handler(CallbackQueryHandler(home.drink_water, pattern="^drink_"))
    app.add_handler(CallbackQueryHandler(home.rest, pattern="^rest_"))
    app.add_handler(CallbackQueryHandler(home.craft_food, pattern="^craft_"))
    app.add_handler(CallbackQueryHandler(home.upgrade_home, pattern="^upgrade_home$"))
    
    # Museum callbacks
    app.add_handler(CallbackQueryHandler(museum.view_trophies, pattern="^museum_trophies$"))
    app.add_handler(CallbackQueryHandler(museum.add_trophy, pattern="^add_trophy_"))
    app.add_handler(CallbackQueryHandler(museum.museum_leaderboard, pattern="^museum_lb$"))
    app.add_handler(CallbackQueryHandler(museum.achievements, pattern="^achievements$"))
    
    # Weapon callbacks
    app.add_handler(CallbackQueryHandler(weapons.buy_weapon, pattern="^buy_weapon_"))
    app.add_handler(CallbackQueryHandler(weapons.equip_weapon, pattern="^equip_weapon_"))
    
    # Inventory callbacks
    app.add_handler(CallbackQueryHandler(inventory.view_items, pattern="^inv_items$"))
    app.add_handler(CallbackQueryHandler(inventory.view_animals, pattern="^inv_animals$"))
    app.add_handler(CallbackQueryHandler(inventory.use_item, pattern="^use_item_"))
    
    # === ADMIN HANDLERS ===
    app.add_handler(CommandHandler("admin", dashboard.admin_panel))
    app.add_handler(CallbackQueryHandler(dashboard.admin_dashboard, pattern="^admin_dashboard$"))
    
    # Admin sub-menus
    app.add_handler(CallbackQueryHandler(manage_content.menu, pattern="^admin_content$"))
    app.add_handler(CallbackQueryHandler(economy.menu, pattern="^admin_economy$"))
    app.add_handler(CallbackQueryHandler(players.menu, pattern="^admin_players$"))
    app.add_handler(CallbackQueryHandler(events.menu, pattern="^admin_events$"))
    app.add_handler(CallbackQueryHandler(transactions.menu, pattern="^admin_transactions$"))
    app.add_handler(CallbackQueryHandler(bot_settings.menu, pattern="^admin_settings$"))
    app.add_handler(CallbackQueryHandler(logs.menu, pattern="^admin_logs$"))
    app.add_handler(CallbackQueryHandler(roles.menu, pattern="^admin_roles$"))
    
    # Admin content management
    app.add_handler(CallbackQueryHandler(manage_content.manage_animals, pattern="^content_animals$"))
    app.add_handler(CallbackQueryHandler(manage_content.add_animal, pattern="^add_animal$"))
    app.add_handler(CallbackQueryHandler(manage_content.edit_animal, pattern="^edit_animal_"))
    app.add_handler(CallbackQueryHandler(manage_content.delete_animal, pattern="^del_animal_"))
    app.add_handler(CallbackQueryHandler(manage_content.manage_weapons, pattern="^content_weapons$"))
    app.add_handler(CallbackQueryHandler(manage_content.add_weapon, pattern="^add_weapon$"))
    app.add_handler(CallbackQueryHandler(manage_content.edit_weapon, pattern="^edit_weapon_"))
    app.add_handler(CallbackQueryHandler(manage_content.manage_items, pattern="^content_items$"))
    app.add_handler(CallbackQueryHandler(manage_content.manage_maps, pattern="^content_maps$"))
    app.add_handler(CallbackQueryHandler(manage_content.toggle_map, pattern="^toggle_map_"))
    app.add_handler(CallbackQueryHandler(manage_content.manage_homes, pattern="^content_homes$"))
    app.add_handler(CallbackQueryHandler(manage_content.manage_museum, pattern="^content_museum$"))
    
    # Admin economy
    app.add_handler(CallbackQueryHandler(economy.set_prices, pattern="^eco_prices$"))
    app.add_handler(CallbackQueryHandler(economy.topup_packages, pattern="^eco_topup$"))
    app.add_handler(CallbackQueryHandler(economy.rarity_multiplier, pattern="^eco_rarity$"))
    app.add_handler(CallbackQueryHandler(economy.toggle_event, pattern="^eco_event_"))
    
    # Admin players
    app.add_handler(CallbackQueryHandler(players.search_player, pattern="^player_search$"))
    app.add_handler(CallbackQueryHandler(players.give_coins, pattern="^player_coins_"))
    app.add_handler(CallbackQueryHandler(players.give_item, pattern="^player_item_"))
    app.add_handler(CallbackQueryHandler(players.set_level, pattern="^player_level_"))
    app.add_handler(CallbackQueryHandler(players.ban_player, pattern="^player_ban_"))
    app.add_handler(CallbackQueryHandler(players.broadcast, pattern="^player_broadcast$"))
    
    # Admin events
    app.add_handler(CallbackQueryHandler(events.create_event, pattern="^event_create$"))
    app.add_handler(CallbackQueryHandler(events.spawn_boss, pattern="^event_boss$"))
    app.add_handler(CallbackQueryHandler(events.active_bosses, pattern="^event_active$"))
    
    # Admin transactions
    app.add_handler(CallbackQueryHandler(transactions.verify_topup, pattern="^txn_verify$"))
    app.add_handler(CallbackQueryHandler(transactions.approve_topup, pattern="^approve_txn_"))
    app.add_handler(CallbackQueryHandler(transactions.reject_topup, pattern="^reject_txn_"))
    app.add_handler(CallbackQueryHandler(transactions.history, pattern="^txn_history$"))
    app.add_handler(CallbackQueryHandler(transactions.export_csv, pattern="^txn_export$"))
    
    # Admin bot settings
    app.add_handler(CallbackQueryHandler(bot_settings.set_photo, pattern="^setting_photo_"))
    app.add_handler(CallbackQueryHandler(bot_settings.game_params, pattern="^setting_params$"))
    app.add_handler(CallbackQueryHandler(bot_settings.toggle_feature, pattern="^setting_toggle_"))
    
    # Admin logs
    app.add_handler(CallbackQueryHandler(logs.realtime_log, pattern="^log_realtime$"))
    app.add_handler(CallbackQueryHandler(logs.cheat_detection, pattern="^log_cheat$"))
    
    # Admin roles
    app.add_handler(CallbackQueryHandler(roles.add_admin, pattern="^role_add$"))
    app.add_handler(CallbackQueryHandler(roles.edit_role, pattern="^role_edit_"))
    app.add_handler(CallbackQueryHandler(roles.remove_admin, pattern="^role_remove_"))
    
    # Conversation handlers for input
    from handlers.conversations import (
        search_conv, p2p_conv, broadcast_conv,
        add_animal_conv, add_weapon_conv, set_price_conv,
        player_action_conv, event_conv, boss_conv, topup_conv
    )
    
    app.add_handler(search_conv)
    app.add_handler(p2p_conv)
    app.add_handler(broadcast_conv)
    app.add_handler(add_animal_conv)
    app.add_handler(add_weapon_conv)
    app.add_handler(set_price_conv)
    app.add_handler(player_action_conv)
    app.add_handler(event_conv)
    app.add_handler(boss_conv)
    app.add_handler(topup_conv)
    
    # Photo handler for admin uploads
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.User(ADMIN_IDS),
        manage_content.handle_photo_upload
    ))
    
    logger.info("🦌 HuntGame Bot starting...")
    await app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())
