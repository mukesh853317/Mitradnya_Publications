import streamlit as st

def run_calculator(selected_adj):
    st.markdown("---")
    
    # ---------------------------------------------------------
    # 1. Existing Complex Calculators (Your Original Code)
    # ---------------------------------------------------------
    if selected_adj == "Goods Lost by Fire" or selected_adj == "Insured Goods Lost by Fire" or selected_adj == "Uninsured Goods Lost by Fire":
        st.subheader(f"📊 Calculator: {selected_adj}")
        col1, col2 = st.columns(2)
        with col1:
            total_value = st.number_input("Total Value of Goods Lost (Rs.)", min_value=0, value=10000, step=100)
        with col2:
            claim_admitted = st.number_input("Insurance Claim Admitted (Rs.) (Enter 0 if uninsured)", min_value=0, value=8000, step=100)
        
        actual_loss = total_value - claim_admitted
        
        st.success("✅ **Accounting Effects**")
        st.write(f"**1. Trading A/c (Credit Side):** Rs. {total_value} (Gross Loss)")
        if claim_admitted > 0:
            st.write(f"**2. Balance Sheet (Assets Side):** Rs. {claim_admitted} (Claim Receivable)")
        st.write(f"**3. Profit & Loss A/c (Debit Side):** Rs. {actual_loss} (Actual Net Loss)")

    elif selected_adj == "Bad Debts":
        st.subheader("📊 Calculator: Bad Debts and RDD (The Master Formula)")
        c1, c2, c3 = st.columns(3)
        with c1:
            debtors = st.number_input("Sundry Debtors (Rs.)", value=50000, step=1000)
            old_bd = st.number_input("Old Bad Debts (Trial Bal.) (Rs.)", value=1000, step=100)
        with c2:
            old_rdd = st.number_input("Old RDD (Trial Bal.) (Rs.)", value=1500, step=100)
            new_bd = st.number_input("New Bad Debts (Adj.) (Rs.)", value=2000, step=100)
        with c3:
            new_rdd_pct = st.number_input("New RDD (%)", value=5.0, step=1.0)
            
        new_rdd_amt = (debtors - new_bd) * (new_rdd_pct / 100)
        pnl_charge = old_bd + new_bd + new_rdd_amt - old_rdd
        net_debtors = debtors - new_bd - new_rdd_amt
        
        st.success("✅ **Final Calculations**")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("**1. Profit & Loss A/c (Debit Side)**")
            st.write(f"➕ Old Bad Debts: Rs. {old_bd}")
            st.write(f"➕ New Bad Debts: Rs. {new_bd}")
            st.write(f"➕ New RDD Amount: Rs. {new_rdd_amt}")
            st.write(f"➖ Old RDD: Rs. {old_rdd}")
            st.info(f"**Total Charge to P&L = Rs. {pnl_charge}**")
        with col_res2:
            st.markdown("**2. Balance Sheet (Assets Side)**")
            st.write(f"Sundry Debtors: Rs. {debtors}")
            st.write(f"➖ Less: New Bad Debts: Rs. {new_bd}")
            st.write(f"➖ Less: New RDD: Rs. {new_rdd_amt}")
            st.info(f"**Net Debtors (Outer Col) = Rs. {net_debtors}**")

    elif selected_adj == "Unrecorded Sales":
        st.subheader("📊 Calculator: Unrecorded Sales (Chain Effect)")
        c1, c2 = st.columns(2)
        with c1:
            debtors = st.number_input("Sundry Debtors (Rs.)", value=10000, step=500)
            unrecorded_sales = st.number_input("Unrecorded Sales Amount (Rs.)", value=2000, step=500)
        with c2:
            new_bd = st.number_input("New Bad Debts (Rs.)", value=1000, step=100)
            rdd_pct = st.number_input("RDD (%)", value=5.0, step=1.0)
            
        debtors_after_sales = debtors + unrecorded_sales
        debtors_after_bd = debtors_after_sales - new_bd
        new_rdd_amt = debtors_after_bd * (rdd_pct / 100)
        net_debtors = debtors_after_bd - new_rdd_amt
        
        st.success("✅ **Calculation Chain (Balance Sheet - Assets Side):**")
        st.write(f"**Step 1:** Initial Debtors = Rs. {debtors}")
        st.write(f"**Step 2:** Add Unrecorded Sales (Rs. {unrecorded_sales}) ➡️ **New Total: Rs. {debtors_after_sales}**")
        st.write(f"**Step 3:** Less New Bad Debts (Rs. {new_bd}) ➡️ **Remaining: Rs. {debtors_after_bd}**")
        st.write(f"**Step 4:** Less New RDD ({rdd_pct}%) ➡️ **Rs. {new_rdd_amt}**")
        st.info(f"**Final Net Debtors (Outer Col) = Rs. {net_debtors}**")

    elif selected_adj == "Unrecorded Purchases":
        st.subheader("📊 Calculator: Unrecorded Purchases")
        c1, c2 = st.columns(2)
        with c1:
            purchases = st.number_input("Purchases (Rs.)", value=40000, step=1000)
            creditors = st.number_input("Sundry Creditors (Rs.)", value=20000, step=1000)
        with c2:
            unrec_purchases = st.number_input("Unrecorded Purchases Amt (Rs.)", value=5000, step=500)
            
        total_purchases = purchases + unrec_purchases
        total_creditors = creditors + unrec_purchases
        
        st.success("✅ **Accounting Effects:**")
        st.markdown("**1. Trading A/c (Debit Side)**")
        st.info(f"Purchases (Rs. {purchases}) ➕ Unrecorded (Rs. {unrec_purchases}) = **Total Rs. {total_purchases}**")
        st.markdown("**2. Balance Sheet (Liabilities Side)**")
        st.info(f"Creditors (Rs. {creditors}) ➕ Unrecorded (Rs. {unrec_purchases}) = **Total Rs. {total_creditors}**")

    elif selected_adj == "Dishonour of Bills":
        st.subheader("📊 Calculator: Bills Receivable Dishonoured")
        st.info("💡 Trick: Both Effects of this Adjustment occur on the Asset Side of the Balance Sheet!")
        c1, c2 = st.columns(2)
        with c1:
            debtors = st.number_input("Sundry Debtors (Rs.)", value=25000, step=1000)
            bills_rec = st.number_input("Bills Receivable (Rs.)", value=10000, step=1000)
        with c2:
            dishonoured_amt = st.number_input("Dishonoured Bill Amount (Rs.)", value=2000, step=500)
            rdd_pct = st.number_input("New RDD (%)", value=5.0, step=1.0)

        net_bills_rec = bills_rec - dishonoured_amt
        new_debtors_total = debtors + dishonoured_amt
        new_rdd_amt = new_debtors_total * (rdd_pct / 100)
        net_debtors = new_debtors_total - new_rdd_amt

        st.success("✅ **Balance Sheet (Assets Side) Effects:**")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("**1. Effect on Bills Receivable**")
            st.write(f"Bills Receivable: Rs. {bills_rec}")
            st.write(f"➖ Less: Dishonoured Bill: Rs. {dishonoured_amt}")
            st.info(f"**Net Bills Receivable = Rs. {net_bills_rec}**")
        with col_res2:
            st.markdown("**2. Effect on Sundry Debtors & RDD**")
            st.write(f"Sundry Debtors: Rs. {debtors}")
            st.write(f"➕ Add: Dishonoured Bill: Rs. {dishonoured_amt}")
            st.write(f"*(Revised Debtors for RDD = Rs. {new_debtors_total})*")
            st.write(f"➖ Less: New RDD ({rdd_pct}%): Rs. {new_rdd_amt}")
            st.info(f"**Final Net Debtors = Rs. {net_debtors}**")

    elif selected_adj == "Wages Included in Machine":
        st.subheader("📊 Calculator: Capital Expenditure in Revenue Expenditure")
        st.info("💡 Trick: Deduct the wrong expense from Trading A/c (e.g. Wages) and ADD it to Balance Sheet (e.g. Machinery). Then deduct Depreciation on the increased amount!")
        c1, c2 = st.columns(2)
        with c1:
            wages = st.number_input("Wages (Trading A/c) (Rs.)", value=15000, step=1000)
            machinery = st.number_input("Machinery (Balance Sheet) (Rs.)", value=50000, step=1000)
        with c2:
            wrong_amt = st.number_input("Installation Charges (Wrongly added in Wages) (Rs.)", value=5000, step=500)
            dep_pct = st.number_input("Depreciation on Machinery (%)", value=10.0, step=1.0)

        net_wages = wages - wrong_amt
        new_machinery = machinery + wrong_amt
        dep_amt = new_machinery * (dep_pct / 100)
        net_machinery = new_machinery - dep_amt

        st.success("✅ **Accounting Effects:**")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("**1. Trading A/c (Debit Side)**")
            st.write(f"Wages: Rs. {wages}")
            st.write(f"➖ Less: Installation of Machinery: Rs. {wrong_amt}")
            st.info(f"**Net Wages to Outer Column = Rs. {net_wages}**")
        with col_res2:
            st.markdown("**2. Balance Sheet (Assets Side)**")
            st.write(f"Machinery: Rs. {machinery}")
            st.write(f"➕ Add: Installation Charges: Rs. {wrong_amt}")
            st.write(f"*(Revised Machinery Value = Rs. {new_machinery})*")
            st.write(f"➖ Less: Depreciation ({dep_pct}%): Rs. {dep_amt}")
            st.info(f"**Net Machinery to Outer Col = Rs. {net_machinery}**")

    elif selected_adj == "Deferred Revenue":
        st.subheader("📊 Calculator: Deferred Revenue Expenditure")
        st.info("💡 Trick: Divide total expenses by total years. One year goes to P&L, remaining years go to Balance Sheet (Assets) as Prepaid!")
        c1, c2 = st.columns(2)
        with c1:
            total_adv = st.number_input("Total Advertisement Expense Paid (Rs.)", min_value=1000, value=50000, step=1000)
        with c2:
            total_years = st.number_input("Paid for how many years?", min_value=2, value=5, step=1)

        yearly_expense = total_adv / total_years
        prepaid_adv = total_adv - yearly_expense

        st.success("✅ **Accounting Effects:**")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.markdown("**1. Profit & Loss A/c (Debit Side)**")
            st.write(f"Advertisement (Total): Rs. {total_adv:,.0f}")
            st.write(f"➖ Less: Prepaid ({total_years - 1} Years): Rs. {prepaid_adv:,.0f}")
            st.info(f"**Current Year Expense = Rs. {yearly_expense:,.0f}**")
        with col_res2:
            st.markdown("**2. Balance Sheet (Assets Side)**")
            st.write(f"Prepaid Advertisement")
            st.write(f"*(For remaining {total_years - 1} years)*")
            st.info(f"**Net Asset Value = Rs. {prepaid_adv:,.0f}**")

    # ---------------------------------------------------------
    # 2. NEW Hidden Adjustments Calculators
    # ---------------------------------------------------------
    elif selected_adj == "Int on Capital" or selected_adj == "Aditional Capital":
        st.subheader("📊 Calculator: Interest on Capital")
        capital = st.number_input("Enter Capital Amount (Rs.):", min_value=0.0, value=100000.0, step=1000.0)
        rate = st.number_input("Enter Rate of Interest (% p.a.):", min_value=0.0, value=5.0, step=0.5)
        months = st.number_input("Enter Months Used (out of 12):", min_value=1.0, max_value=12.0, value=12.0, step=1.0)
        
        interest = (capital * rate / 100) * (months / 12)
        st.success(f"✅ **Calculated Interest:** Rs. {interest:,.2f}")
        st.info("**P&L A/c:** DEBIT side | **Balance Sheet:** ADD to Capital")

    elif selected_adj == "Int on Drawing":
        st.subheader("📊 Calculator: Interest on Drawings (6 Months Trap)")
        drawings = st.number_input("Enter Total Drawings Amount (Rs.):", min_value=0.0, value=10000.0, step=1000.0)
        rate = st.number_input("Enter Rate of Interest (% p.a.):", min_value=0.0, value=10.0, step=0.5)
        
        interest = (drawings * rate / 100) * (6 / 12)  # Compulsory 6 months
        st.success(f"✅ **Calculated Interest (for Average 6 Months):** Rs. {interest:,.2f}")
        st.info("**P&L A/c:** CREDIT side | **Balance Sheet:** LESS from Capital")

    elif selected_adj == "Rent / Salary Paid (10 Months)":
        st.subheader("📊 Calculator: Hidden Outstanding Expense")
        amount = st.number_input("Enter Amount Paid in Trial Balance (Rs.):", min_value=0.0, value=10000.0, step=1000.0)
        paid_months = st.number_input("Enter Number of Months Paid (e.g., 10):", min_value=1.0, max_value=11.0, value=10.0, step=1.0)
        
        missing_months = 12 - paid_months
        outstanding = (amount / paid_months) * missing_months
        total_expense = amount + outstanding
        st.success(f"✅ **Outstanding for {int(missing_months)} months:** Rs. {outstanding:,.2f}")
        st.info(f"**P&L A/c (DEBIT):** Rs. {total_expense:,.2f} | **Balance Sheet (LIABILITIES):** Rs. {outstanding:,.2f}")

    elif selected_adj == "Prepaid Insurance 15 months":
        st.subheader("📊 Calculator: Prepaid Insurance (15 Months)")
        amount = st.number_input("Enter Total Insurance Paid for 15 Months (Rs.):", min_value=0.0, value=15000.0, step=1000.0)
        
        prepaid_amount = (amount / 15) * 3 
        pnl_amount = amount - prepaid_amount
        st.success(f"✅ **Prepaid Insurance (for 3 extra months):** Rs. {prepaid_amount:,.2f}")
        st.info(f"**P&L A/c (LESS):** Rs. {pnl_amount:,.2f} | **Balance Sheet (ASSETS):** Rs. {prepaid_amount:,.2f}")

    elif selected_adj == "10% Govt Bonds":
        st.subheader("📊 Calculator: 10% Govt Bonds (Hidden Interest)")
        amount = st.number_input("Enter Investment Amount (Rs.):", min_value=0.0, value=50000.0, step=1000.0)
        months = st.number_input("Enter Months Held up to 31st March (e.g., 6 for Oct):", min_value=1.0, max_value=12.0, value=6.0, step=1.0)
        
        accrued = (amount * 10 / 100) * (months / 12)
        st.success(f"✅ **Accrued Interest (Income):** Rs. {accrued:,.2f}")
        st.info("**P&L A/c:** CREDIT side | **Balance Sheet:** ADD to Investment (ASSETS)")

    elif selected_adj == "Int on Partners Loan":
        st.subheader("📊 Calculator: Interest on Partner's Loan (The 6% Trap)")
        amount = st.number_input("Enter Partner's Loan Amount (Rs.):", min_value=0.0, value=50000.0, step=1000.0)
        months = st.number_input("Enter Months Used up to 31st March (e.g., 6):", min_value=1.0, max_value=12.0, value=6.0, step=1.0)
        st.warning("⚠️ **Critical Rule:** 6% p.a. compulsory if rate is not given!")
        
        interest = (amount * 6 / 100) * (months / 12)
        st.success(f"✅ **Calculated Interest (at 6%):** Rs. {interest:,.2f}")
        st.info("**P&L A/c:** DEBIT side | **Balance Sheet:** ADD to Loan (LIABILITIES)")

    # ---------------------------------------------------------
    # 3. Topics with No Calculators (Motivational Quotes & Tips)
    # ---------------------------------------------------------
    elif selected_adj == "Depreciation":
        st.info("📝 **Mukesh Sir's Study Tip:** Depreciation is simply a decrease in the value of an asset. Just multiply the asset value by the given percentage. Don't forget to check the date of purchase for new assets!")
        st.success("🌟 *'Success is the sum of small efforts, repeated day in and day out.'* Keep practicing!")
        
    elif selected_adj == "Goods Distribued as Free Sample":
        st.info("📝 **Mukesh Sir's Study Tip:** Free samples are a form of advertisement. Credit the Trading A/c (as goods are going out) and Debit the P&L A/c (as it is an advertisement expense).")
        st.success("🌟 *'The expert in anything was once a beginner.'* You are on the right track!")

    else:
        st.info("📝 **Keep Going!** Review the infographic above carefully. Understanding the logic is more important than just memorizing!")
        st.success("🌟 *'Education is the most powerful weapon which you can use to change the world.'* - Nelson Mandela")
