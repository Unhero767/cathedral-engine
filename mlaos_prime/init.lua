-- ====================================================================
-- MLAOS-Prime :: Neovim Sovereign Configuration (init.lua)
-- Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
-- ====================================================================

-- Leader Key
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Core Options
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.smartindent = true
vim.opt.termguicolors = true
vim.opt.scrolloff = 8
vim.opt.signcolumn = "yes"
vim.opt.updatetime = 50

-- Basic Keymaps
vim.keymap.set("n", "<leader>pv", vim.cmd.Ex, { desc = "Open Netrw Explorer" })
vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save File" })
vim.keymap.set("n", "<leader>q", ":q<CR>", { desc = "Quit Buffer" })

-- Status Inscription
vim.api.nvim_create_autocmd("VimEnter", {
    callback = function()
        print("MLAOS-Prime Neovim Substrate Initialized [Lex I Active]")
    end,
})
