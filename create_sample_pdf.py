#!/usr/bin/env python3
"""
Create a sample PDF document for testing the Asset Data Privacy frontend.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_sample_pdf():
    """Create a sample financial document PDF."""
    
    # Create the PDF document
    doc = SimpleDocTemplate("sample_financial_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("QUARTERLY FINANCIAL REPORT", title_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph("This report provides a comprehensive overview of our financial performance for Q3 2024.", normal_style))
    story.append(Spacer(1, 10))
    
    # Financial Metrics
    story.append(Paragraph("Key Financial Metrics", heading_style))
    
    metrics_data = [
        ['Metric', 'Value', 'Change'],
        ['Total Revenue', '$45,750,000', '+12.5%'],
        ['Operating Costs', '$32,250,000', '+8.2%'],
        ['Net Income', '$13,500,000', '+18.7%'],
        ['EBITDA', '$18,250,000', '+15.3%'],
        ['Cash Flow', '$22,100,000', '+22.1%']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2*inch, 1.5*inch, 1*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 20))
    
    # Investment Portfolio
    story.append(Paragraph("Investment Portfolio Overview", heading_style))
    story.append(Paragraph("Our investment portfolio continues to demonstrate strong performance across all asset classes.", normal_style))
    story.append(Spacer(1, 10))
    
    portfolio_data = [
        ['Asset Class', 'Allocation', 'Value', 'Performance'],
        ['MasterFund1', '35%', '$16,012,500', '+18.2%'],
        ['AlphaFund', '25%', '$11,437,500', '+15.7%'],
        ['StrategicFund', '20%', '$9,150,000', '+12.8%'],
        ['GrowthFund', '15%', '$6,862,500', '+20.1%'],
        ['Cash Reserve', '5%', '$2,287,500', '+2.1%']
    ]
    
    portfolio_table = Table(portfolio_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1*inch])
    portfolio_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(portfolio_table)
    story.append(Spacer(1, 20))
    
    # Risk Metrics
    story.append(Paragraph("Risk Assessment", heading_style))
    
    risk_data = [
        ['Risk Metric', 'Current Value', 'Target Range', 'Status'],
        ['Volatility', '12.5%', '8-15%', 'Within Range'],
        ['Sharpe Ratio', '1.85', '>1.5', 'Excellent'],
        ['Maximum Drawdown', '-4.2%', '<-5%', 'Good'],
        ['VaR (95%)', '-2.8%', '<-3%', 'Excellent'],
        ['Beta', '0.95', '0.8-1.2', 'Within Range']
    ]
    
    risk_table = Table(risk_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.3*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 20))
    
    # Market Analysis
    story.append(Paragraph("Market Analysis", heading_style))
    story.append(Paragraph("The current market environment presents both opportunities and challenges for our portfolio strategy.", normal_style))
    story.append(Spacer(1, 10))
    
    market_analysis = [
        "• Equity markets continue to show resilience despite economic headwinds",
        "• Fixed income yields remain attractive for income generation",
        "• Alternative investments provide diversification benefits",
        "• Currency fluctuations impact international holdings",
        "• Commodity prices show mixed performance across sectors"
    ]
    
    for point in market_analysis:
        story.append(Paragraph(point, normal_style))
    
    story.append(Spacer(1, 20))
    
    # Outlook
    story.append(Paragraph("Outlook and Recommendations", heading_style))
    story.append(Paragraph("Based on our analysis, we recommend maintaining our current asset allocation while monitoring key risk factors.", normal_style))
    story.append(Spacer(1, 10))
    
    recommendations = [
        "• Maintain overweight position in growth assets",
        "• Increase allocation to defensive sectors",
        "• Consider tactical adjustments based on market conditions",
        "• Monitor interest rate sensitivity",
        "• Review currency hedging strategies"
    ]
    
    for rec in recommendations:
        story.append(Paragraph(rec, normal_style))
    
    # Build the PDF
    doc.build(story)
    print("Sample PDF created: sample_financial_report.pdf")

if __name__ == "__main__":
    create_sample_pdf()
