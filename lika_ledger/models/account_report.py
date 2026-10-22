import io
import xlsxwriter
from odoo import models, _

class AccountReport(models.Model):
    _inherit = 'account.report'

    def export_to_xlsx(self, options, response=None):
        # 1. Verify if this is the General Ledger report
        is_gl = (
            self.custom_handler_model_id.model == 'account.general.ledger.handler' or
            self == self.env.ref('account_reports.general_ledger_report', raise_if_not_found=False)
        )

        if not is_gl:
            return super().export_to_xlsx(options, response=response)

        # 2. Force unfold all lines to retrieve transaction details
        options = dict(options)
        options['unfold_all'] = True

        # 3. Generate Dynamic File Name (Company Name + Date Range)
        date_str = options.get('date', {}).get('string', '')
        company_name = self.env.company.name
        file_name = f"{self.name} - {company_name} ({date_str}).xlsx" if date_str else f"{self.name} - {company_name}.xlsx"

        # 4. Initialize XLSX Workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet_name = (self.name or 'General Ledger')[:31]
        sheet = workbook.add_worksheet(sheet_name)

        # Formats
        title_style = workbook.add_format({'bold': True, 'font_size': 14})
        header_style = workbook.add_format({
            'bold': True,
            'bg_color': '#E9ECEF',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        cell_style = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'top'})
        num_style = workbook.add_format({'border': 1, 'align': 'right', 'num_format': '#,##0.00'})

        # --- Title Row (Replaced with Year) ---
        year = ''
        if date_str and len(date_str) == 4 and date_str.isdigit():
            year = date_str
        else:
            date_from = options.get('date', {}).get('date_from', '')
            if date_from:
                year = date_from[:4]
            else:
                date_to = options.get('date', {}).get('date_to', '')
                if date_to:
                    year = date_to[:4]
        
        if year:
            sheet.write(0, 4, year, title_style)

        # 5. Build Dynamic Table Column Headers
        headers = [_('Code'), _('Account Name'), _('Reference'), _('Description')]
        if self.column_ids:
            headers.extend([col.name for col in self.column_ids])
        else:
            headers.extend([_('Date'), _('Partner'), _('Debit'), _('Credit'), _('Balance')])

        for col_idx, header in enumerate(headers):
            sheet.write(2, col_idx, header, header_style)

        # 6. Fetch Unfolded Report Lines
        report_lines = self._get_lines(options)

        current_code = ""
        current_account_name = ""
        row_idx = 3

        for line in report_lines:
            line_id = str(line.get('id', ''))
            is_account_header = line.get('level') == 1 or line.get('unfoldable', False)

            if is_account_header:
                line_name = line.get('name', '')
                # Split "112006 Account Receivable" into Code and Account Name
                parts = line_name.split(' ', 1)
                current_code = parts[0] if len(parts) > 0 else ''
                current_account_name = parts[1] if len(parts) > 1 else ''

                # Write parent Account row
                sheet.write(row_idx, 0, current_code, cell_style)
                sheet.write(row_idx, 1, current_account_name, cell_style)
                sheet.write(row_idx, 2, '', cell_style) # Empty Reference
                sheet.write(row_idx, 3, '', cell_style) # Empty Description

                # Write Account level summary totals across columns (starting from Col E / index 4)
                columns = line.get('columns', [])
                col_offset = 4
                for col in columns:
                    val = col.get('no_format', col.get('name', ''))
                    if isinstance(val, (int, float)):
                        sheet.write(row_idx, col_offset, val, num_style)
                    else:
                        sheet.write(row_idx, col_offset, str(val) if val is not None else '', cell_style)
                    col_offset += 1
                row_idx += 1
                continue

            # --- Detail Row (Transactions / Initial Balance) ---
            line_name = line.get('name', '')
            
            # FIX: Extract Reference as the string just before the first "(" if it exists
            if '(' in line_name:
                # Split at the first occurrence of '('
                ref, desc_part = line_name.split('(', 1)
                ref = ref.strip()
                desc = '(' + desc_part.strip() # Keep the opening bracket in the description
            else:
                ref = ''
                desc = line_name.strip()

            # Col A: Code
            sheet.write(row_idx, 0, current_code, cell_style)
            # Col B: Account Name
            sheet.write(row_idx, 1, current_account_name, cell_style)
            # Col C: Reference
            sheet.write(row_idx, 2, ref, cell_style)
            # Col D: Description
            sheet.write(row_idx, 3, desc, cell_style)

            # Columns E onward (Date, Partner, Debit, Credit, Balance)
            columns = line.get('columns', [])
            col_offset = 4
            for col in columns:
                val = col.get('no_format', col.get('name', ''))
                if isinstance(val, (int, float)):
                    sheet.write(row_idx, col_offset, val, num_style)
                else:
                    sheet.write(row_idx, col_offset, str(val) if val is not None else '', cell_style)
                col_offset += 1

            row_idx += 1

        # 7. Set Column Widths
        sheet.set_column(0, 0, 10)  # Code
        sheet.set_column(1, 1, 30)  # Account Name
        sheet.set_column(2, 2, 20)  # Reference
        sheet.set_column(3, 3, 40)  # Description
        sheet.set_column(4, len(headers) - 1, 16) # Dynamic columns

        workbook.close()
        output.seek(0)
        generated_file = output.read()
        output.close()

        # 8. Return file stream payload with formatted file_name
        return {
            'file_name': file_name,
            'file_content': generated_file,
            'file_type': 'xlsx',
        }